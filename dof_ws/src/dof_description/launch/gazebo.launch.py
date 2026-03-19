from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
import xacro
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Get share directory for dof_description
    share_dir = get_package_share_directory('dof_description')

    # Process URDF from xacro -> ensures meshes resolve correctly
    xacro_file = os.path.join(share_dir, 'urdf', 'dof.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    # Simulation time
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Gazebo package path
    gazebo_pkg = get_package_share_directory('ros_gz_sim')

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_urdf},
            {'use_sim_time': use_sim_time},
        ]
    )

    # Launch Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_pkg, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'verbose': 'true', 'use_sim_time': use_sim_time, 'gz_args': '-r empty.sdf'}.items()
    )

    # ros2_control node
    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[xacro_file, os.path.join(share_dir, 'config', 'controllers.yaml')],
        output='screen'
    )

    # Spawn robot into Gazebo from /robot_description topic
    urdf_spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'dof',
            '-topic', 'robot_description'
        ],
        output='screen'
    )

    # ROS-Gazebo bridge
    bridge_params = os.path.join(share_dir, 'config', 'gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Controller spawners (delay to wait for /clock)
    joint_broad_spawner = TimerAction(
        period=5.0,
        actions=[Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_state_broadcaster"],
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}]
        )]
    )

    position_control_spawner = TimerAction(
        period=5.0,
        actions=[Node(
            package="controller_manager",
            executable="spawner",
            arguments=["dof_controller"],
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}]
        )]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation time'),
        robot_state_publisher_node,
        gazebo,
        urdf_spawn_node,
        ros_gz_bridge,
        joint_broad_spawner,
        position_control_spawner
    ])
