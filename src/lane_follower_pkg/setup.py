from setuptools import find_packages, setup

package_name = 'lane_follower_pkg'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Keszthelyi Arpad',
    maintainer_email='arpad.keszthelyi@gmail.com',
    description='Modularis OpenCV alapu savkoveto ROS 2 csomag.',
    license='GPL-3.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'lane_follower_node = lane_follower_pkg.lane_follower_node:main',
        ],
    },
)
