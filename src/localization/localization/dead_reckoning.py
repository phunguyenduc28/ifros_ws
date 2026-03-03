import math

from geometry_msgs.msg import TransformStamped

import numpy as np

import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster

from turtlesim.msg import Pose

from nav_msgs.msg import Odometry

from sensor_msgs.msg import JointState


def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q



class DeadReckoning(Node):
    def __init__(self):
        super().__init__('dead_reckoning')

        # Robot constants
        self.wheel_radius = 0.035
        self.wheel_base_distance = 0.230
        self.wheel_vel_noise = np.array([0.01, 0.01])
        self.left_wheel_joint_name = 'turtlebot/wheel_left_joint'
        self.right_wheel_joint_name = 'turtlebot/wheel_right_joint'
        self.prediction_time = 0.05

        self.v_left = None
        self.v_right = None
        # Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # callback function on each message
        self.joint_state_sub = self.create_subscription(
            JointState,
            f'/turtlebot/joint states',
            self.turtlebot_join_state_callback,
            1)

        self.odom_pub = self.create_publisher(Odometry, '/turtlebot/dead_reck_odom', 10)
        self.timer = self.create_timer(self.prediction_time, self.dead_reckoning)

    def turtlebot_join_state_callback(self, msg):
        joint_state_velocity = msg.velocity
        self.v_left = joint_state_velocity[joint_state_velocity.index(self.left_wheel_joint_name)]
        self.v_right = joint_state_velocity[joint_state_velocity.index(self.right_wheel_joint_name)]        

    def dead_reckoning(self):
        if self.v_left is None or self.v_right is None:
            return
        
        # t = TransformStamped()

        # # Read message content and assign it to
        # # corresponding tf variables
        # t.header.stamp = self.get_clock().now().to_msg()
        # t.header.frame_id = 'world'
        # t.child_frame_id = self.turtlename

        # # Turtle only exists in 2D, thus we get x and y translation
        # # coordinates from the message and set the z coordinate to 0
        # t.transform.translation.x = msg.x
        # t.transform.translation.y = msg.y
        # t.transform.translation.z = 0.0

        # # For the same reason, turtle can only rotate around one axis
        # # and this why we set rotation in x and y to 0 and obtain
        # # rotation in z axis from the message
        # q = quaternion_from_euler(0, 0, msg.theta)
        # t.transform.rotation.x = q[0]
        # t.transform.rotation.y = q[1]
        # t.transform.rotation.z = q[2]
        # t.transform.rotation.w = q[3]

        # # Send the transformation
        # self.tf_broadcaster.sendTransform(t)

    







def main():
    rclpy.init()
    node = DeadReckoning()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()