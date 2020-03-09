#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import sys, select, termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def talker():
    pub = rospy.Publisher('/turtlesim/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1000) #10Hz 
    while not rospy.is_shutdown():
        if getKey() == params["forward"]:
            vel.linear.x = 1
        if getKey() == params["back"]:
            vel.linear.x = -1
        if getKey() == params["left"]:
            vel.angular.z = -1
        if getKey() == params["right"]:
            vel.angular.z = 1

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass