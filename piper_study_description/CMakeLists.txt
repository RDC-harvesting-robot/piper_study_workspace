cmake_minimum_required(VERSION 2.8.3)

project(piper_study_description)

find_package(catkin REQUIRED)

catkin_package()

find_package(roslaunch)

foreach(dir urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
