#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import sys, select, termios, tty

def getKey():      #funkcja zwracajaca wcisniety klawisz, niestety nie udalo nam sie utworzyc prostszej
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSANOW, termios.tcgetattr(sys.stdin.fileno()))
    return key

def talker():     #funkcja publikujaca wiadomosci do wezla zolwia
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)    #ustawienie podstawowych atrybutow
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(100)
    twist = Twist()     #utworzenie obiektu wiadomosci
    while not rospy.is_shutdown():
        keycode = getKey()     #odczytanie i przypisanie wcisnietego klawisza
        #sprawdzenie, czy wcisniety klawisz odpowiada ktoremus z ustawionych w parametrach
        #jesli tak, to w zaleznosci od klawisza, polozenie zolwia zmienia sie liniowo badz biegunowo
        if keycode == rospy.get_param("/forward"):
            twist.linear.x = 2
            twist.angular.z = 0
        elif keycode == rospy.get_param("/back"):
            twist.linear.x = -2
            twist.angular.z = 0
        elif keycode == rospy.get_param("/left"):
            twist.angular.z = 2
            twist.linear.x = 0
        elif keycode == rospy.get_param("/right"):
            twist.angular.z = -2
            twist.linear.x = 0
        #jesli zostanie wcisniete 'ctrl+c' program konczy dzialanie
        elif keycode == "\x03":
        	rospy.signal_shutdown("Pressed CTRL-c. Killing node.")
        #jesli nie, to polozenie zolwia nie ulega zmianie
        else:
            twist.linear.x = 0
            twist.angular.z = 0
        pub.publish(twist)    #publikacja wiadomosci

if __name__ == '__main__':    #uzycie funkcji publikujacej wiadomosci
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
