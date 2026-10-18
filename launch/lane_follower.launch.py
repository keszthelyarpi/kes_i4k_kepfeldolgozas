from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    show_gui_arg = DeclareLaunchArgument(
        'show_gui',
        default_value='True',
        description='OpenCV GUI ablakok megjelenítése (True / False)'
    )

    v4l2_camera_node = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='v4l2_camera_node',
        output='screen',
        parameters=[{
            'video_device': '/dev/video0',
            'image_size': [640, 480],
            'pixel_format': 'YUYV'
        }]
    )

    lane_follower_node = Node(
        package='lane_follower_pkg',
        executable='lane_follower_node',
        name='lane_follower_node',
        output='screen',
        parameters=[{
            'show_gui': LaunchConfiguration('show_gui'),
        }]
    )

    return LaunchDescription([
        show_gui_arg,
        v4l2_camera_node,
        lane_follower_node,
    ])
