#!/usr/bin/env python

import rospy
import json
import os
from tf.transformations import *
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker

#sprawdzenie poprawnosci polozenia dla kazdego zlacza
def checkPosition(data):
    if data.position[0] < bounds['i1'][0] or data.position[0] > bounds['i1'][1]:
        return False
    if data.position[1] < bounds['i2'][0] or data.position[1] > bounds['i2'][1]:
        return False
    if data.position[2] < bounds['i3'][0] or data.position[2] > bounds['i3'][1]:
        return False
    return True

def simpleKinematics(data):
    #jesli polozenie jest niepoprawne zostaje wypisana informacja
    if not checkPosition(data):
        rospy.logerr('Wrong position: ' + str(data))
        return

    axis_x, axis_z = (1, 0, 0), (0, 0, 1)

    #utworzenie trzech kolejnych macierzy z parametrow D-H
    a, d, alpha, theta = params['i1']
    translation_z = translation_matrix((0, 0, d))
    rotation_z = rotation_matrix(data.position[0], axis_z)
    translation_x = translation_matrix((a, 0, 0))
    rotation_x = rotation_matrix(alpha, axis_x)
    matrix1 = concatenate_matrices(rotation_x, translation_x, rotation_z, translation_z)

    a, d, alpha, theta = params['i2']
    translation_z = translation_matrix((0, 0, d))
    rotation_z = rotation_matrix(data.position[1], axis_z)
    translation_x = translation_matrix((a, 0, 0))
    rotation_x = rotation_matrix(alpha, axis_x)
    matrix2 = concatenate_matrices(rotation_x, translation_x, rotation_z, translation_z)

    a, d, alpha, theta = params['i3']
    translation_z = translation_matrix((0, 0, data.position[2]-d))
    rotation_z = rotation_matrix(theta, axis_z)
    translation_x = translation_matrix((a, 0, 0))
    rotation_x = rotation_matrix(alpha, axis_x)
    matrix3 = concatenate_matrices(rotation_x, translation_x, rotation_z, translation_z)

    #utworzenie macierzy kinematyki prostej i przeliczenie na translacje i rotacje koncowki
    final_matrix = concatenate_matrices(matrix1, matrix2, matrix3)
    x, y, z = translation_from_matrix(final_matrix)
    quaternion_x, quaternion_y, quaternion_z, quaternion_w = quaternion_from_matrix(final_matrix)

    #utworzenie i nadanie wiadomosci z polozeniem koncowki
    pose = PoseStamped()
    pose.header.frame_id = 'base'
    pose.header.stamp = rospy.Time.now()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose.pose.orientation.x = quaternion_x
    pose.pose.orientation.y = quaternion_y
    pose.pose.orientation.z = quaternion_z
    pose.pose.orientation.w = quaternion_w
    pub.publish(pose)

if __name__ == '__main__':
    #utworzenie wezla
    rospy.init_node('NONKDL_DKIN', anonymous=True)
    pub = rospy.Publisher('non_kdl_msgs', PoseStamped, queue_size=10)
    rospy.Subscriber('joint_states', JointState, simpleKinematics)

    #pobranie parametrow i ograniczen
    params = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../MDH_wartosci.json', 'r') as file:
        params = json.loads(file.read())

    bounds = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../bounds.json', 'r') as file:
        bounds = json.loads(file.read())

    rospy.spin()