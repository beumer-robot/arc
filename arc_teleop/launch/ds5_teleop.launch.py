"""
Launch file for launching everything necessary for the DS5 controller to work
input -> Joy -> Twist
By using the ds5_driver package, including the nodes:
- ds5_driver_node
- joy_to_twist_node
Through their respective launch files (ds5_driver.launch.py and joy_to_twist.launch.py)
"""
import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os


def generate_launch_description():
    pkg_name = "ds5_driver"
    pkg_path = get_package_share_directory(pkg_name)

    config_pkg_name = "arc_teleop"
    config_pkg_path = get_package_share_directory(config_pkg_name)

    ds5_driver_config_file_name = "ds5_driver_params.yaml"
    joy_to_twist_config_file_name = "joy_to_twist_params.yaml"

    # Declare the log level argument
    log_level = "info"

    # Include the launch files for the ds5_driver and joy_to_twist nodes
    ds5_driver_launch_file = os.path.join(
        pkg_path,
        "launch",
        "ds5_driver.launch.py",
    )
    joy_to_twist_launch_file = os.path.join(
        pkg_path,
        "launch",
        "joy_to_twist.launch.py",
    )

    # Include and pass the config files to the launch files
    ds5_driver_config_file = os.path.join(
        config_pkg_path,
        "config",
        ds5_driver_config_file_name,
    )
    joy_to_twist_config_file = os.path.join(
        config_pkg_path,
        "config",
        joy_to_twist_config_file_name,
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "ds5_driver_config_file",
                default_value=ds5_driver_config_file,
                description="Path to the ROS2 parameters file to use for the ds5_driver node",
            ),
            DeclareLaunchArgument(
                "joy_to_twist_config_file",
                default_value=joy_to_twist_config_file,
                description="Path to the ROS2 parameters file to use for the joy_to_twist node",
            ),
            DeclareLaunchArgument(
                "log_level",
                default_value=log_level,
                description="Logging level",
            ),
            launch.actions.IncludeLaunchDescription(
                launch.launch_description_sources.PythonLaunchDescriptionSource(
                    ds5_driver_launch_file
                ),
                launch_arguments={
                    "config_file": LaunchConfiguration("ds5_driver_config_file"),
                    "log_level": LaunchConfiguration("log_level"),
                }.items(),
            ),
            launch.actions.IncludeLaunchDescription(
                launch.launch_description_sources.PythonLaunchDescriptionSource(
                    joy_to_twist_launch_file
                ),
                launch_arguments={
                    "config_file": LaunchConfiguration("joy_to_twist_config_file"),
                    "log_level": LaunchConfiguration("log_level"),
                }.items(),
            ),
        ]
    )
