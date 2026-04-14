import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    pkg_path = get_package_share_directory('amr_bot')

    # Process xacro → URDF string
    xacro_file = os.path.join(pkg_path, 'urdf', 'amr_bot.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()
    # Get world file path
    world_file = os.path.join(pkg_path, 'worlds', 'room.world')


    # Launch Gazebo with our room world
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', world_file, '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    # robot_state_publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}]
    )

    # Spawn robot into Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'amr_bot',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.155'
        ]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
    ])