

## Dependencies
 - rclpy
 - turtlesim

## How to run
```sh
git clone https://github.com/A-K-O-R-A/intro_task_ds
cd intro_task_ds

colcon build
# Change the ending depending on your shell
source install/setup.zsh
 
ros2 launch color_changer sim_launch.py  
```

In a different terminal you can now control the turtle with `ros2 run turtlesim turtle_teleop_key`