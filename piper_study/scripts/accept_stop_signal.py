#!/usr/bin/env python3
import rospy
import copy
from moveit_commander import MoveGroupCommander, RobotCommander, PlanningSceneInterface
from geometry_msgs.msg import Pose, WrenchStamped
from std_msgs.msg import Bool
from tf.transformations import quaternion_from_euler


class MoveitOscillator:
    def __init__(self):
        rospy.init_node("moveit_force_stop_oscillator", anonymous=True)

        # MoveIt 初期化
        self.robot = RobotCommander()
        self.scene = PlanningSceneInterface()
        self.move_group = MoveGroupCommander("arm")
        rospy.loginfo(f"Initialized MoveGroupCommander for group: {self.move_group.get_name()}")

        # 停止判定用
        self.stop_flag = False

        # しきい値
        self.force_threshold = 10.0  # N（適宜調整）

        # サブスクライバ
        rospy.Subscriber("/stop_signal", Bool, self.stop_callback)
        rospy.Subscriber("/force_data", WrenchStamped, self.force_callback)

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

        # Pose B
        self.pose_b = copy.deepcopy(self.pose_a)
        self.pose_b.position.y += 0.2

    def stop_callback(self, msg):
        if msg.data:
            rospy.logwarn("STOP signal received.")
            self.stop_flag = True
            self.move_group.stop()

    def force_callback(self, msg: WrenchStamped):
        force = msg.wrench.force
        magnitude = (force.x**2 + force.y**2 + force.z**2) ** 0.5
        rospy.logdebug(f"Force magnitude: {magnitude:.2f} N")

        if magnitude > self.force_threshold:
            rospy.logwarn(f"Force exceeded threshold: {magnitude:.2f} N > {self.force_threshold}")
            self.stop_flag = True
            self.move_group.stop()

    def move_to(self, pose):
        if self.stop_flag:
            return False
        self.move_group.set_pose_target(pose)

        success, plan, _, _ = self.move_group.plan()
        if not success or plan is None:
            rospy.logwarn("Planning failed.")
            self.move_group.clear_pose_targets()
            return False

        rospy.loginfo("Executing trajectory...")
        self.move_group.execute(plan, wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()
        return True

    def start_oscillation(self):
        rospy.loginfo("Starting oscillation with force monitoring...")
        while not rospy.is_shutdown() and not self.stop_flag:
            rospy.loginfo("→ Moving to Pose A")
            if not self.move_to(self.pose_a):
                break
            rospy.sleep(1.0)

            rospy.loginfo("→ Moving to Pose B")
            if not self.move_to(self.pose_b):
                break
            rospy.sleep(1.0)

        rospy.loginfo("Motion stopped due to force or signal.")

if __name__ == "__main__":
    try:
        controller = MoveitOscillator()
        controller.start_oscillation()
    except rospy.ROSInterruptException:
        pass
