# piper_study_workspace

## Environment
ROS noetic (Ubuntu20.04)

## piper (robot arm)

### Install
```
cd ~/catkin_ws/src/
git clone https://github.com/open-rdc/Piper_ros
git clone https://github.com/yasuohayashibara/piper_study_workspace
cd ~/catkin_ws/
catkin build
source ~/catkin_ws/devel/setup.bash
```

### Execute
```
roslaunch piper_moveit_config demo_gazebo.launch
```

## real sense (sensor)

### Install
```
cd ~/catkin_ws/src
git clone --recurse-submodules https://github.com/RDC-harvesting-robot/realsense-ros-gazebo
sudo apt install ros-noetic-ddynamic-reconfigure ros-noetic-realsense2-camera
cd ~/catkin_ws
catkin build
source devel/setup.bash
```

### Execute (sample)
```
roslaunch realsense2_description view_d435_model_rviz_gazebo.launch
```
