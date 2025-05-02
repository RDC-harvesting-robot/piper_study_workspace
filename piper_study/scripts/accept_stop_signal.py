#!/usr/bin/env python3
import rospy
import copy
from moveit_commander import MoveGroupCommander, RobotCommander, PlanningSceneInterface
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool
from tf.transformations import quaternion_from_euler


class MoveitOscillator:
    def __init__(self):
        rospy.init_node("moveit_oscillator_node", anonymous=True)

        # MoveIt 初期化
        self.robot = RobotCommander()
        self.scene = PlanningSceneInterface()
        self.move_group = MoveGroupCommander("arm")  # ← Piperのグループ名
        rospy.loginfo(f"Initialized MoveGroupCommander for group: {self.move_group.get_name()}")

        # 停止信号
        self.stop_flag = False
        rospy.Subscriber("/stop_signal", Bool, self.stop_callback)

        # Pose A
        self.pose_a = Pose()
        self.pose_a.position.x = 0.3
        self.pose_a.position.y = 0.0
        self.pose_a.position.z = 0.3
        q = quaternion_from_euler(0, 1.57, 0)
        self.pose_a.orientation.x = q[0]
        self.pose_a.orientation.y = q[1]
        self.pose_a.orientation.z = q[2]
        self.pose_a.orientation.w = q[3]

        # Pose B（左右方向へ移動）
        self.pose_b = copy.deepcopy(self.pose_a)
        self.pose_b.position.y += 0.2

    def stop_callback(self, msg):
        if msg.data:
            rospy.logwarn("STOP signal received.")
            self.stop_flag = True
            self.move_group.stop()

    def move_to(self, pose):
        if self.stop_flag:
            return False
        self.move_group.set_pose_target(pose)

        # 計画チェック
        success, plan, _, _ = self.move_group.plan()
        if not success or plan is None:
            rospy.logwarn("Planning failed.")
            self.move_group.clear_pose_targets()
            return False

        # 実行
        rospy.loginfo("Executing trajectory...")
        self.move_group.execute(plan, wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()
        return True

    def start_oscillation(self):
        rospy.loginfo("Starting oscillation between Pose A and Pose B...")
        while not rospy.is_shutdown() and not self.stop_flag:
            rospy.loginfo("→ Moving to Pose A")
            if not self.move_to(self.pose_a):
                break
            rospy.sleep(1.0)

            rospy.loginfo("→ Moving to Pose B")
            if not self.move_to(self.pose_b):
                break
            rospy.sleep(1.0)

        rospy.loginfo("Oscillation finished or interrupted.")


if __name__ == "__main__":
    try:
        controller = MoveitOscillator()
        controller.start_oscillation()
    except rospy.ROSInterruptException:
        pass
