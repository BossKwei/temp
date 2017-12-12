import rospy
import sensor_msgs.msg


def callback(data):
    data = sensor_msgs.msg.Imu(data)
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)


def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('chatter', sensor_msgs.msg.Imu, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()