#!/usr/bin/python
import time
import rospy
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import buf_fucker.srv


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)


fucker = None


def handle_fit_transform(request):
    start_time = time.time()
    #
    # rospy.loginfo('request arrived, batch size: %d' % (request.batch_size))
    #
    x_data = np.reshape(request.images, [request.batch_size, 1, 28, 28])
    y_data = fucker(Variable(torch.FloatTensor(x_data)))
    y_data = y_data.data.numpy()
    #
    #
    reply = buf_fucker.srv.FitTransformResponse()
    reply.results = np.argmax(y_data, axis=1)
    reply.confidences = (np.max(y_data, axis=1) - np.min(y_data, axis=1)) / (np.max(y_data) - np.min(y_data))
    #
    rospy.loginfo('request batch %d finished, cost time: %f' % (request.batch_size, (time.time() - start_time)))
    return reply


def main():
    rospy.init_node('buf_fucker')
    # init
    model = rospy.get_param('~model', 'checkpoint.pth.tar')
    rospy.loginfo('using model %s', model)
    # init cnn
    use_cuda = False
    global fucker
    fucker = Net()
    if use_cuda:
        fucker.cuda()
    checkpoint = torch.load(model)
    fucker.load_state_dict(checkpoint['state_dict'])
    fucker.eval()
    #
    server = rospy.Service(name='~FitTransform', service_class=buf_fucker.srv.FitTransform,
                                  handler=handle_fit_transform)
    rospy.loginfo('server ready')
    #
    rospy.loginfo('convolution neural nwtwork fucker ready')
    #
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as e:
        rospy.loginfo(e)
    except rospy.ROSException as e:
        rospy.logerr(e)
