import sys



from turtlesim.msg import Pose
from rcl_interfaces.msg import Parameter, SetParameters, ParameterValue

import rclpy
from rclpy.node import Node

import math

class ColorClient(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        
        self.subscription = self.create_subscription(Pose, "/turtle1/pose", self.listener, 10)
        self.last_x = 0;
        self.last_y = 0;

        self.cli = self.create_client(SetParameters, '/turtlesim/set_parameters')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = SetParameters.Request()

    def listener(self, msg: Pose):
        # Check if there is movement
        x_mov = (self.last_x - msg.x) != 0;
        y_mov = (self.last_y - msg.y) != 0;

        # Check if there should be movement
        s_mov = msg.linear_velocity != 0
        s_x_mov = s_mov and (math.cos(msg.theta) != 0);
        s_y_mov = s_mov and (math.sin(msg.theta) != 0);

        # Check if the turtle touched the borders on one of the axis
        x_border = x_mov != s_x_mov;
        y_border = y_mov != s_y_mov;

        if y_border:
            if msg.y == 0:
                # bottom
                self.send_request(255, 128, 0)
            else:
                # top
                self.send_request(255, 0, 0)
        elif x_border:
            if msg.x == 0:
                # left
                self.send_request(0, 0, 255)
            else:
                # right
                self.send_request(0, 255, 0)
                

        self.last_x = msg.x;
        self.last_y = msg.y;

    def send_request(self, r, g, b):
        
        self.req.parameters = [
            Parameter(name='background_r', value=ParameterValue(type=2, integer_value=int(r))),
            Parameter(name='background_g', value=ParameterValue(type=2, integer_value=int(g))),
            Parameter(name='background_b', value=ParameterValue(type=2, integer_value=int(b)))
        ]
        
        self.future = self.cli.call_async(self.req)

def main():
    rclpy.init()

    color_client = ColorClient()

    rclpy.spin(color_client)
    color_client.destroy_node()
    rclpy.shutdown()

"""

if __name__ == '__main__':
    main()