#!/usr/bin/env python

import rospy
import time
from interpolacja.srv import Interpolation
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math

#wartosci poczatkowe
current_position = [0,0,0]
frequency = 50

#funkcja interpolujaca
def handleInterpolation(data):
    #sprawdzenie danych
    if data.time <= 0 or not -1.57075 <= data.j1 <= 1.57075 or not -1.57075 <= data.j2 <= 1.57075 or not -0.2 <= data.j3 <= 0.2:
        return False
    #zapisanie danych o robocie i interpolacji
    new_position = [data.j1, data.j2, data.j3]
    rate = rospy.Rate(frequency)
    j1, j2, j3 = current_position[0], current_position[1], current_position[2]
    frames_number = int(math.ceil(data.time * frequency))
    current_time = 0.
    #interpolacja
    for i in range(0, frames_number + 1):
        current_position[0] = interpolation(j1, new_position[0], data.time, current_time, data.style)
        current_position[1] = interpolation(j2, new_position[1], data.time, current_time, data.style)
        current_position[2] = interpolation(j3, new_position[2], data.time, current_time, data.style)
        current_time = current_time + 1. / frequency
        rate.sleep()
    return True

#sprawdzenie rodzaju interpolacji
def interpolation(first, last, time, current_time, style):
    if style == 'complex':
        return complexInterpolation(first, last, time, current_time)
    else:
        return simpleInterpolation(first, last, time, current_time)

#interpolacja prostym sposobem
def simpleInterpolation(first, last, time, current_time):
    return first + (float(last - first) / time) * current_time

#interpolacja zlozonym sposobem
def complexInterpolation(first, last, time, current_time):
    h = 2. * float(last - first) / time
    ratio = h / (time / 2.)
    if current_time < time / 2.:
        return first + current_time**2 * ratio / 2.
    else:
        return last - (time-current_time)**2 * ratio / 2.

#funkcja publikujaca transformacje
def jointPublisher():
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    srv = rospy.Service('int', Interpolation, handleInterpolation)
    rospy.init_node('int_srv')
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