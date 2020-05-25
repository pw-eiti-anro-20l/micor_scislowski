#!/usr/bin/env python

import sys
import rospy
from interpolacja.srv import Interpolation

#funkcja rzadajaca interpolacji robota
def interpolationClient(j1, j2, j3, time, style):
    rospy.wait_for_service('int')
    try:
        interpolation = rospy.ServiceProxy('int', Interpolation)
        response = interpolation(j1, j2, j3, time, style)
        return response.status
    except rospy.ServiceException, e:
        print "Service failed: %s"%e

if __name__ == "__main__":
    #wczytanie danych interpolacji robota
    j1 = float(sys.argv[1])
    j2 = float(sys.argv[2])
    j3 = float(sys.argv[3])
    time = float(sys.argv[4])
    style = sys.argv[5]
    print "Requesting interpolation."
    #rozpoczecie serwisu interpolacji robota
    print interpolationClient(j1, j2, j3, time, style)