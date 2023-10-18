import sys


from tut_inter.srv import AddThreeInts

from turtlesim.msg import Pose
from turtlesim.srv import SetPen


from rcl_interfaces.msg import Parameter
from rcl_interfaces.srv import SetParameters, GetParameters, ListParameters
from rcl_interfaces.msg import ParameterDescriptor, ParameterValue

import rclpy
from rclpy.node import Node

import math

class MinimalClientAsync(Node):

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
        # Is there movement
        x_mov = (self.last_x - msg.x) != 0;
        y_mov = (self.last_y - msg.y) != 0;

        # Should there be movement
        s_mov = msg.linear_velocity != 0
        s_x_mov = s_mov and (math.cos(msg.theta) != 0);
        s_y_mov = s_mov and (math.sin(msg.theta) != 0);
        
        # Touched borders on axis
        x_border = x_mov != s_x_mov;
        y_border = y_mov != s_y_mov;

        if y_border:
            if msg.y == 0:
                # bottom
                self.send_request(255, 55, 55)
            else:
                # top
                self.send_request(255, 0, 0)

        if x_border:
            if msg.x == 0:
                if y_border:
                    if msg.y == 0:
                        print("bot left")
                    else:
                        print("top left")
            else:
                if y_border:
                    if msg.y == 0:
                        print("bot right")
                    else:
                        print("bot left")

        self.last_x = msg.x;
        self.last_y = msg.y;

    def send_request(self, r, g, b):
        self.req.parameters = [
            Parameter(name='background_r', value=ParameterValue(integer_value=int(r))),
            Parameter(name='background_g', value=ParameterValue(integer_value=int(g))),
            Parameter(name='background_b', value=ParameterValue(integer_value=int(b)))
        ]
        self.future = self.cli.call_async(self.req)

def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    # response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    # minimal_client.get_logger().info(
     #   'Result of add_three_ints: for %d + %d + %d = %d' %
     #   (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), response.sum))

    rclpy.spin(minimal_client)
    minimal_client.destroy_node()
    rclpy.shutdown()

"""
def callback(data):
   rospy.loginfo("I heard %s",data.data)
    
def listener():
    rospy.init_node('node_name')
    rospy.Subscriber("chatter", String, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
"""

if __name__ == '__main__':
    main()