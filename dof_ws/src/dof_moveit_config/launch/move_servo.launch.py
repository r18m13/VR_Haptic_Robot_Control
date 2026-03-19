from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    moveit_pkg = get_package_share_directory('dof_moveit_config')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Move Group Node (only SRDF needed, no OMPL required)
    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[
            os.path.join(moveit_pkg, 'config', 'moveit_controllers.yaml'),  # your controllers
            {'use_sim_time': use_sim_time}
        ]
    )

    # MoveIt Servo Node
    moveit_servo_node = Node(
        package='moveit_servo',
        executable='servo_node',
        output='screen',
        parameters=[
            os.path.join(moveit_pkg, 'config', 'servo.yaml'),
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        move_group_node,
        moveit_servo_node
    ])
