#!/usr/bin/env python3
import rospy
from moveit_commander import MoveGroupCommander, PlanningSceneInterface, RobotCommander
from geometry_msgs.msg import Pose

if __name__ == "__main__":
    rospy.init_node("move_group_interface_tutorial", anonymous=True)

    # Initialize moveit_commander
    robot = RobotCommander()
    scene = PlanningSceneInterface()
    move_group_arm = MoveGroupCommander("arm")
    move_group_gripper = MoveGroupCommander("gripper")

    rospy.loginfo("Available Planning Groups:")
    rospy.loginfo(robot.get_group_names())

    # 1. Move to home position
    # move_group_arm.set_named_target("home")
    # plan_arm = move_group_arm.plan()
    # success = move_group_arm.execute(plan_arm, wait=True)
    # rospy.loginfo("Moving to home position: %s", "SUCCESS" if success else "FAILED")

    # 2. Place the TCP above the blue box

    target_joint = [0.0, 0.01, -0.01, 0.0, 0.0, 0.0]
    move_group_arm.set_joint_value_target(target_joint)
    move_group_arm.go(wait=True)
    move_group_arm.stop()

    # 2. Place the TCP above the blue box
    target_joint = [1.57, 0.01, -0.01, 0.0, 0.0, 0.0]
    move_group_arm.set_joint_value_target(target_joint)
    move_group_arm.go(wait=True)
    move_group_arm.stop()

    print(move_group_arm.get_current_pose().pose)

    # 2. Place the TCP above the blue box
    current_pose = move_group_arm.get_current_pose().pose
    target_pose1 = Pose()
    target_pose1.orientation = current_pose.orientation
    target_pose1.position.x = current_pose.position.x
    target_pose1.position.y = current_pose.position.y
    target_pose1.position.z = current_pose.position.z + 0.2
    move_group_arm.set_pose_target(target_pose1)
    move_group_arm.go(wait=True)
    move_group_arm.stop()
    move_group_arm.clear_pose_targets()

    # 3. Open the gripper
    move_group_gripper.set_named_target("open")
    plan_gripper = move_group_gripper.plan()
    success = move_group_gripper.execute(plan_gripper, wait=True)
    rospy.loginfo("Opening gripper: %s", "SUCCESS" if success else "FAILED")

    # 4. Move the TCP close to the object
    target_pose1.position.z -= 0.2
    move_group_arm.set_pose_target(target_pose1)
    plan_arm = move_group_arm.plan()
    success = move_group_arm.execute(plan_arm, wait=True)
    rospy.loginfo("Moving TCP close to the object: %s", "SUCCESS" if success else "FAILED")

    # 5. Close the gripper
    move_group_gripper.set_named_target("closed")
    plan_gripper = move_group_gripper.plan()
    success = move_group_gripper.execute(plan_gripper, wait=True)
    rospy.loginfo("Closing gripper: %s", "SUCCESS" if success else "FAILED")

    # 6. Move the TCP above the plate
    target_pose1.position.z += 0.2
    target_pose1.position.x -= 0.6
    move_group_arm.set_pose_target(target_pose1)
    plan_arm = move_group_arm.plan()
    success = move_group_arm.execute(plan_arm, wait=True)
    rospy.loginfo("Moving TCP above the plate: %s", "SUCCESS" if success else "FAILED")

    # 7. Lower the TCP above the plate
    target_pose1.position.z -= 0.14
    move_group_arm.set_pose_target(target_pose1)
    plan_arm = move_group_arm.plan()
    success = move_group_arm.execute(plan_arm, wait=True)
    rospy.loginfo("Lowering TCP above the plate: %s", "SUCCESS" if success else "FAILED")

    # 8. Open the gripper
    move_group_gripper.set_named_target("open")
    plan_gripper = move_group_gripper.plan()
    success = move_group_gripper.execute(plan_gripper, wait=True)
    rospy.loginfo("Opening gripper: %s", "SUCCESS" if success else "FAILED")

    rospy.loginfo("Task completed!")
    rospy.signal_shutdown("Task completed")
