import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'aquatic_comms'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AQUADRIVE AI Team',
    maintainer_email='user@todo.todo',
    description='Hybrid communications manager and Pixhawk failover bridge for Autonomous Aquatic System',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hybrid_comms_node = aquatic_comms.hybrid_comms_node:main',
            'pixhawk_bridge = aquatic_comms.pixhawk_bridge:main',
            'sitl_failover_tester = aquatic_comms.sitl_failover_tester:main',
            'vision_node = aquatic_comms.vision_node:main',
            'geofence_guard = aquatic_comms.geofence_guard:main',
            'battery_health_monitor = aquatic_comms.battery_health_monitor:main',
        ],
    },
)
