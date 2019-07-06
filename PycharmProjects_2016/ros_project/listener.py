#!/usr/bin/env python

import rospy
import mavros_msgs.msg


def mavros_state_callback(data):
    # data = mavros_msgs.msg.State(data)
    print(data.mode)
    print(data.armed)
    print(data.connected)
    print(data.guided)


def listener():
    rospy.init_node('listener')
    rospy.Subscriber('/mavros/state', mavros_msgs.msg.State, mavros_state_callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
