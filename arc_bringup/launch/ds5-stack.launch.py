"""
Launch file to launch the entire control stack using the DS5 controller.
This means including the launch file from arc_teleop:
- ros2 launch arc_teleop ds5_teleop.launch.py
Setting up the ros bridge server from the rosbridge_server package:
- ros2 launch rosbridge_server rosbridge_websocket_launch.xml
Furthermore, it requires launching the twist_to_diff_drive node from arc_base
along with the low_level_motor_controller nodes from arc_base.
- ros2 run arc_base twist_to_diff_drive_node
- low_level_motor_controller_left
- low_level_motor_controller_right
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch_yaml.launch_description_sources import YAMLLaunchDescriptionSource

from pathlib import Path
import pathlib

CMAP = {
    "red": "\033[0;31m",
    "green": "\033[0;32m",
    "yellow": "\033[0;33m",
    "blue": "\0330;34m",
    "magenta": "\0330;35m",
    "nc": "\033[0m",
}


def green(text):
    return CMAP["green"] + text + CMAP["nc"]


def red(text):
    return CMAP["red"] + text + CMAP["nc"]


def generate_launch_description():
    # The ROS Bridge Server to connect to Foxglove Studio
    rosbridge_server = IncludeLaunchDescription(
        XMLLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("rosbridge_server"),
                "launch",
                "rosbridge_websocket_launch.xml",
            )
        )
    )

    # The DS5 controller
    ds5_teleop = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("arc_teleop"),
                "launch",
                "ds5_teleop.launch.py",
            )
        )
    )

    base_config = os.path.join(
        get_package_share_directory("arc_bringup"), "config", "params.yaml"
    )

    # twist to diff drive
    twist_to_diff_drive = Node(
        package="arc_base",
        executable="twist_to_diff_drive_node",
        name="twist_to_diff_drive",
        parameters=[base_config],
    )

    print(green("config: " + base_config))

    # low level motor controller for left motor
    low_level_motor_controller_left = Node(
        package="arc_base",
        executable="low_level_motor_controller",
        name="low_level_motor_controller_left",
        output="screen",
        # prefix="gdb -ex run --args",
        parameters=[base_config],
    )

    # low level motor controller for right motor
    low_level_motor_controller_right = Node(
        package="arc_base",
        executable="low_level_motor_controller",
        name="low_level_motor_controller_right",
        parameters=[base_config],
    )

    return LaunchDescription(
        [
            rosbridge_server,
            ds5_teleop,
            twist_to_diff_drive,
            low_level_motor_controller_left,
            low_level_motor_controller_right,
        ]
    )
