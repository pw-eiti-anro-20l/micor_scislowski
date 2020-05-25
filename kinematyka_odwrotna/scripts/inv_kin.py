#!/usr/bin/env python

import rospy
import json
import os
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from math import *

current_position = [0, 0, 0]

def invertedKinematics(data):
    params = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../MDH_wartosci.json', 'r') as file:
        params = json.loads(file.read())

    x = data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z

    if z>=1.3 and z<=1.7:
        j3 = -z + 1.5
    else:
        rospy.logerr('Wrong position!')
        return

    d = sqrt(x**2 + y**2)
    a1 = atan2(y, x)
    try:
        a2 = acos((-params['i3'][0]**2 + params['i2'][0]**2 + d**2) / (2 * params['i2'][0] * d))
        a3 = acos((params['i2'][0]**2 + params['i3'][0]**2 - d**2) / (2 * params['i2'][0] * params['i3'][0]))
    except:
        rospy.logerr('Wrong position!')
        return
    j1 = a1 + a2
    j2 = -pi + a3

    current_position[0] = j1
    current_position[1] = j2
    current_position[2] = j3

def jointPublisher():
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    sub = rospy.Subscriber('interpolation', PoseStamped, invertedKinematics)
    rospy.init_node('ikin_node')
    rate = rospy.Rate(100)
    joint_state = JointState()
    while not rospy.is_shutdown():
        joint_state.header = Header()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['base_to_link_1', 'link_1_to_link_2', 'link_2_to_tool']
        joint_state.position = current_position
        joint_state.velocity = [0,0,0]
        joint_state.effort = [0,0,0]
        pub.publish(joint_state)

if __name__ == "__main__":
    try:
        jointPublisher()
    except rospy.ROSInterruptException:
        pass