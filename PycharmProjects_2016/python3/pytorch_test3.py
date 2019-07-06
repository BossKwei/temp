import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np


m = nn.Dropout2d(p=0.2)
input = Variable(torch.randn(2, 2))
output = m(input)

print(input)
print(output)

