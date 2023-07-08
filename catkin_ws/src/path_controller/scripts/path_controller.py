#! /usr/bin/env python3
import rospy 
from geometry_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
import random
import math
from gazebo_msgs.msg import *
import numpy as np
import csv
import rospkg
import matplotlib.pyplot as plt
from matplotlib import cm
import time
from environment import Env
import math
from tf.transformations import euler_from_quaternion

odometry = Odometry()

def odometry_callback(data):
	global odometry
	odometry = data

if __name__ == "__main__": 
    rospy.init_node("path_controller_node", anonymous=False)
    
    rospy.Subscriber('odom', Odometry, odometry_callback)
    
    env = Env()
    state_scan = env.reset()
    action = np.zeros(2)

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)    
    r = rospy.Rate(5) # 10hz
    velocity = Twist()
    while not rospy.is_shutdown():
        right_laser = max(state_scan[300:360])
        left_laser = max(state_scan[60:120])
        heading, current_distance = env.move()
        count = 0
        if len(state_scan) > 0:
            if min(state_scan[0:35] > 0.35):
                action[0] = 0.2
                action[1] = heading * 0.5

            else:
                action[0] = 0
                if right_laser > left_laser:
                    action[1] = -.5
                    state_scan = env.step(action)
                else:
                    action[1] = .5
                    state_scan = env.step(action)
        state_scan = env.step(action)
                
        r.sleep()