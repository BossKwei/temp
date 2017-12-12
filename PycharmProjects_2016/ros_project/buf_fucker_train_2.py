from __future__ import print_function
import rospy
import numpy as np
import torch
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

# x_data_csv = np.loadtxt('/home/bosskwei/Desktop/x_data.csv', delimiter=',', dtype=np.float32)
x_data_csv = np.loadtxt('/home/bosskwei/Desktop/x_data.csv', dtype=np.float32)
x_data_csv = np.reshape(x_data_csv, [-1, 28, 28])
x_data_csv = np.expand_dims(x_data_csv, 1)
print(x_data_csv.shape)

# y_label_csv = np.loadtxt('/home/bosskwei/Desktop/y_label.csv', delimiter=',', dtype=np.float32)
y_label_csv = np.loadtxt('/home/bosskwei/Desktop/y_label.csv', dtype=np.float32)
y_label_csv = np.argmax(y_label_csv, axis=1)
print(y_label_csv.shape)

# Training settings
parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                    help='input batch size for training (default: 64)')
parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                    help='input batch size for testing (default: 1000)')
parser.add_argument('--epochs', type=int, default=50, metavar='N',
                    help='number of epochs to train (default: 50)')
parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                    help='learning rate (default: 0.01)')
parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                    help='SGD momentum (default: 0.5)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='enables CUDA training')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='how many batches to wait before logging training status')
args = parser.parse_args()
args.cuda = False

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)

#args.batch_size
kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}
'''
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),
    batch_size=64, shuffle=True, **kwargs)
'''
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=False, transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ]), download=False),
    batch_size=args.batch_size, shuffle=True, **kwargs)


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


model = Net()
if args.cuda:
    model.cuda()

optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)


import random
def get_batch(xs, ys):
    order = list(range(62372))
    random.shuffle(order)
    #
    x_ret = []
    y_ret = []
    #
    for i in range(64):
        x_ret.append(xs[order[i]])
        y_ret.append(ys[order[i]])
    return np.array(x_ret, dtype=np.float32), y_ret


def m_train(epoch):
    model.train()
    #
    #
    for batch_idx in range(2000):
        x_batch, y_batch = get_batch(x_data_csv, y_label_csv)
        #print('x_batch shape: %s', x_batch.shape)
        #print('y_batch shape: %s', y_batch.shape)
        '''
        for batch_idx, (data, target) in enumerate(train_loader):
            if args.cuda:
                data, target = data.cuda(), target.cuda()
            print(target)
        '''
        data, target = Variable(torch.FloatTensor(x_batch)), Variable(torch.LongTensor(y_batch))
        optimizer.zero_grad()
        output = model(data)
        #print(output)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {0}, batch:{1}/2000'.format(epoch, batch_idx))
    torch.save({'state_dict': model.state_dict()}, f='checkpoint-{0}.pth.tar'.format(epoch))


def m_testxxx(epoch):
    # checkpoint = torch.load('checkpoint-1.pth.tar')
    # model.load_state_dict(checkpoint['state_dict'])
    # optimizer.load_state_dict(checkpoint['optimizer'])
    #
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        # x_data = data[0].numpy()
        # x_data = np.reshape(x_data, [28, 28])
        # np.savetxt('./data.csv', x_data)
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data, volatile=True), Variable(target)
        output = model(data)
        test_loss += F.nll_loss(output, target).data[0]
        pred = output.data.max(1)[1]  # get the index of the max log-probability
        #result = pred.numpy()
        #np.reshape(result, [-1, 1])
        #print(result.shape)
        # print(pred)
        correct += pred.eq(target.data).cpu().sum()

    test_loss = test_loss
    test_loss /= len(test_loader)  # loss function already averages over batch size
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


for epoch in range(1, args.epochs + 1):
    m_train(epoch)
    m_testxxx(epoch)
