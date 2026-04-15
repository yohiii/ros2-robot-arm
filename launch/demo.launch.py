from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    robot_arm_path = get_package_share_directory('robot_arm')
    moveit_config_path = get_package_share_directory('robot_arm_moveit_config')

    urdf_file = os.path.join(robot_arm_path, 'urdf', 'arm.urdf')
    srdf_file = os.path.join(moveit_config_path, 'config', 'robot_arm.srdf')
    kinematics_file = os.path.join(moveit_config_path, 'config', 'kinematics.yaml')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    with open(srdf_file, 'r') as f:
        robot_description_semantic = f.read()

    with open(kinematics_file, 'r') as f:
        import yaml
        kinematics_config = yaml.safe_load(f)

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        Node(
            package='moveit_ros_move_group',
            executable='move_group',
            name='move_group',
            parameters=[{
                'robot_description': robot_description,
                'robot_description_semantic': robot_description_semantic,
                'robot_description_kinematics': kinematics_config,
                'moveit_controller_manager': 'moveit_simple_controller_manager/MoveItSimpleControllerManager',
                'moveit_simple_controller_manager': {
                    'controller_names': ['arm_controller'],
                    'arm_controller': {
                        'type': 'FollowJointTrajectory',
                        'action_ns': 'follow_joint_trajectory',
                        'default': True,
                        'joints': ['joint_1', 'joint_2', 'joint_3']
                    }
                }
            }]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
        )
    ])