#!/usr/bin/env python

import rospy
import diagnostic_msgs.msg


def diagnostic_callback(data):
    #data = diagnostic_msgs.msg.DiagnosticArray(data)
    #rospy.loginfo(rospy.get_caller_id() + ': %s', data.status)
    print(data.status[0])


def listener():
    rospy.init_node('px4_listener')
    rospy.Subscriber('/diagnostics', diagnostic_msgs.msg.DiagnosticArray, diagnostic_callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
