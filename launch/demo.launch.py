import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config=os.path.join(get_package_share_directory('badminton_poles_sim'),'rviz','demo.rviz')
    return LaunchDescription([Node(package='badminton_poles_sim', executable='sim', output='screen'),Node(package='rviz2', executable='rviz2', arguments=['-d',config], output='screen')])
