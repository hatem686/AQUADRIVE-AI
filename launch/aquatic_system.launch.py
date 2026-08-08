from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        Node(
            package='aquatic_comms',
            executable='hybrid_comms_node',
            name='hybrid_comms_manager',
            output='screen',
            parameters=[
                {
                    'attenuation_threshold_db': 20.0,
                    'check_interval_sec': 1.0
                }
            ]
        ),

        Node(
            package='aquatic_comms',
            executable='pixhawk_bridge',
            name='pixhawk_failover_bridge',
            output='screen'
        ),

        Node(
            package='aquatic_comms',
            executable='sitl_failover_tester',
            name='sitl_failover_tester',
            output='screen'
        )

    ])
