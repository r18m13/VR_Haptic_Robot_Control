from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    # Build MoveIt config
    moveit_config = (
        MoveItConfigsBuilder(robot_name="dof", package_name="dof_moveit_config")
        .robot_description(file_path="urdf/dof.urdf.xacro")
        .robot_description_semantic(file_path="config/dof.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(
            pipelines=["ompl", "chomp"]
        )
        .robot_description_kinematics(file_path="config/kinematics.yaml")  # optional
        .to_moveit_configs()
    )

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[moveit_config.robot_description]
    )

    # Controller Manager (ros2_control)
    controller_manager_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            moveit_config.robot_description 
        ],
        output="screen"
    )

    # Joint State Broadcaster Spawner
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # DOF Controller Spawner
    dof_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["dof_controller", "--controller-manager", "/controller_manager"],
        output="screen"
    )

    # Move Group Node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.trajectory_execution,
            moveit_config.moveit_cpp
        ]
    )

    # RViz2 Node with custom config
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", str(moveit_config.package_path/"launch/moveit.rviz")],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic
        ]
    )

    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager_node,
        TimerAction(period=3.0, actions=[joint_state_broadcaster_spawner]),
        TimerAction(period=5.0, actions=[dof_controller_spawner]),
        TimerAction(period=6.0, actions=[move_group_node]),
        TimerAction(period=8.0, actions=[rviz_node])
    ])
