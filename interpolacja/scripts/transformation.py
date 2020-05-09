#!/usr/bin/env python

import json
from tf.transformations import *
import rospy
import math

#odczytuje wartosci D-H z pliku oraz je zwraca
def getParams():
    file = open('../MD-H_wartosci.json', 'r')
    params = json.loads(file.read())
    return params

#zapisuje wartosci urdf do odpowiedniego pliku
def setParams(xyz, rpy, mark, a, file, d):
    file.write(mark + ":\n")
    #zapis przeksztalcen zlacz
    file.write("  j_xyz: {} {} {}\n".format(*xyz))
    file.write("  j_rpy: {} {} {}\n".format(*rpy))
    #zapis przeksztalcen i dlugosci czlonow
    file.write("  l_xyz: {} {} {}\n".format(xyz[0] / 2, xyz[1] / 2, xyz[2] / 2))
    if a != 0:
        file.write("  l_rpy: 0 {} 0\n".format(-math.atan(d/a)))
    else:
        file.write("  l_rpy: 0 0 0\n")
    file.write("  l_len: {}\n".format(math.sqrt(a*a + d*d)))

#przeksztalca wartosci D-H w wartosci urdf
def transformation():
    #pobiera parametry
    params = getParams()
    x_axis, z_axis = (1, 0, 0), (0, 0, 1)
    #otwiera plik do zapisu
    file = open('../urdf_wartosci.yaml', 'w')
    for mark in params.keys():
        a, d, alpha, theta = params[mark]
        #tworzy macierze przeksztalcen
        translation_z = translation_matrix((0, 0, d))
        rotation_z = rotation_matrix(theta, z_axis)
        translation_x = translation_matrix((a, 0, 0))
        rotation_x = rotation_matrix(alpha, x_axis)
        matrix = concatenate_matrices(translation_z, rotation_z, translation_x, rotation_x)
        #oblicza translacje i rotacje
        rpy = euler_from_matrix(matrix)
        xyz = translation_from_matrix(matrix)
        #zapisuje dane do pliku
        setParams(xyz, rpy, mark, a, file, d)

if __name__ == '__main__':
    try:
        transformation()
    except rospy.ROSInterruptException:
        pass
