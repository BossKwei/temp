import numpy as np
import matplotlib.pyplot as plt
import skimage.io, skimage.feature, skimage.transform, skimage.draw, skimage.morphology, skimage.color, skimage.filters

x, y, yaw = 120, 120, 0.0
speed_x, speed_y, speed_yaw = 0.0, 0.0, 0.0


def move_1(dx, dy, dyaw):
    global x, y, yaw, speed_x, speed_y, speed_yaw
    speed_x = 0.75 * speed_x + dx
    speed_y = 0.75 * speed_y + dy
    speed_yaw = 0.75 * speed_yaw + dyaw
    x, y, yaw = int(x + speed_x), int(y + speed_y), yaw + speed_yaw
    #
    canvas = np.zeros([640, 640, 3], dtype=np.float32)
    canvas[y - 6:y + 7, x - 6:x + 7] = 1.0, 0, 0
    plt.imshow(canvas)
    plt.draw()
    plt.pause(0.1)


def move_2(throttle, steering):
    global x, y, yaw, speed_x, speed_y, speed_yaw
    # sp(t+1) = 0.75 * sp + alpha => sp = alpha / (z - 1)
    speed_yaw = 0.75 * speed_yaw + steering
    yaw = yaw + speed_yaw
    #
    throttle_x, throttle_y = throttle * np.cos(yaw), throttle * np.sin(yaw)
    speed_x, speed_y = 0.75 * speed_x + throttle_x, 0.75 * speed_y + throttle_y
    x, y = int(x + speed_x), int(y + speed_y)
    #
    canvas = np.zeros([640, 640, 3], dtype=np.float32)
    canvas[y - 6:y + 7, x - 6:x + 7] = 1.0, 0, 0
    plt.imshow(canvas)
    plt.draw()
    plt.pause(0.1)


if __name__ == '__main__':
    while True:
        for _ in range(20):
            move_2(2.0, 0.0)
        for _ in range(20):
            move_2(10.0, 0.5)
