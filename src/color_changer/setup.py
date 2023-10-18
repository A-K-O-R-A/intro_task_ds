from setuptools import find_packages, setup

package_name = 'color_changer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='blank',
    maintainer_email='git@github.com',
    description='Changes the background color of the turtlesim window when the turtle touches the walls',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'client = color_changer.client_member_function:main',
        ],
    },
)
