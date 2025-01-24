cmake_minimum_required(VERSION 2.8.3)

project(piper_study)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package()

find_package(roslaunch)
