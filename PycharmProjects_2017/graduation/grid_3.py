import time
import random
import queue
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import skimage.io, skimage.feature, skimage.transform, skimage.draw, skimage.morphology, skimage.color, skimage.filters


def make_maze(w=81, h=61):
    wall = 255
    route = 0
    # 1
    maze = np.ones([h, w], dtype=np.uint8) * wall
    visited = np.zeros_like(maze, dtype=np.bool)
    edge = np.zeros([h, w, 2], dtype=np.uint32)
    #
    schedule = set()
    x, y = 1, 1
    while True:
        maze[y, x] = route
        visited[y, x] = True
        neighbors = [(x, y - 2), (x, y + 2), (x - 2, y), (x + 2, y)]
        for xx, yy in neighbors:
            if 0 <= xx < w and 0 <= yy < h:
                if visited[yy, xx]:
                    continue
                schedule.add((xx, yy))
                edge[yy, xx] = ((xx + x) // 2, (yy + y) // 2)
        if len(schedule):
            [(x, y)] = random.sample(schedule, 1)
            schedule.remove((x, y))
            xx, yy = edge[y, x]
            maze[yy, xx] = route
        else:
            break
    #
    return maze


def dynamic_programming(maze, src, dst, wall_threshold=0.5):
    h, w = maze.shape
    visited = np.zeros_like(maze, dtype=np.bool)
    trace = np.zeros([h, w, 2], dtype=np.uint32)
    schedule = queue.Queue()
    #
    schedule.put(src)
    while True:
        x, y = schedule.get()
        if visited[y, x]:  # `schedule` may include repeated items
            continue
        visited[y, x] = True
        if (x, y) == dst:
            break
        else:
            for xx, yy in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
                if 0 <= xx < w and 0 <= yy < h:
                    if visited[yy, xx]:
                        continue
                    if maze[yy, xx] > wall_threshold:
                        continue
                    schedule.put((xx, yy))
                    trace[yy, xx] = x, y
    path = []
    xx, yy = dst
    while True:
        path.append((xx, yy))
        x, y = trace[yy, xx]
        if src == (x, y):
            break
        xx, yy = x, y
    path = np.flip(path, axis=0)
    return path


def draw_path(maze, path):
    wall, route = np.max(maze), 0
    canvas = np.copy(maze)
    for x, y in path:
        canvas[y, x] = (wall + route) / 2
    plt.imshow(canvas, cmap='Greys')
    plt.show()


def sliding_window(maze, pt, window_size=(64, 64)):
    wall, route = np.max(maze), 0
    h_maze, w_maze = maze.shape
    #
    x, y = pt
    h_slide, w_slide = window_size
    # expected rect
    top, bottom, left, right = y - h_slide // 2, y + h_slide // 2, x - w_slide // 2, x + w_slide // 2
    # valid rect
    v_top, v_bottom, v_left, v_right = max(top, 0), min(bottom, h_maze), max(left, 0),min(right, w_maze)
    # generate slide window
    sw = np.ones([h_slide, w_slide], dtype=np.uint8) * wall
    sw[v_top - top:h_slide - bottom + v_bottom, v_left - left:w_slide - right + v_right] = \
        maze[v_top:v_bottom, v_left:v_right]
    #
    plt.ioff()
    plt.imshow(sw, cmap='Greys')
    plt.draw()
    plt.pause(0.1)


def rotate_window(maze, pt, yaw, window_size=(64, 64)):
    wall, route = np.max(maze), 0
    h_maze, w_maze = maze.shape
    #
    x, y = pt
    h_slide, w_slide = window_size
    # expected rect
    top, bottom, left, right = y - h_slide // 2, y + h_slide // 2, x - w_slide // 2, x + w_slide // 2
    # valid rect
    v_top, v_bottom, v_left, v_right = max(top, 0), min(bottom, h_maze), max(left, 0), min(right, w_maze)
    # generate slide window
    sw = np.ones([h_slide, w_slide], dtype=np.float32) * wall
    sw[v_top - top:h_slide - bottom + v_bottom, v_left - left:w_slide - right + v_right] = \
        maze[v_top:v_bottom,v_left:v_right]
    # rotation
    rr, cc = skimage.draw.circle(31, 31, 32)
    # circle = np.zeros_like(sw, dtype=np.bool)
    # circle[rr, cc] = True
    # circle = np.bitwise_not(circle)
    # sw = np.multiply(sw, circle)
    rw = np.ones_like(sw)
    rw[rr, cc] = sw[rr, cc]
    rw = skimage.transform.rotate(rw, yaw)
    #
    plt.ioff()
    plt.imshow(rw, cmap='Greys')
    plt.draw()
    plt.pause(0.1)


def main_1():
    w, h = 21, 21
    maze = make_maze(w, h)
    w, h = 240, 240
    maze = skimage.transform.resize(maze, (h, w), mode='edge')
    #
    while True:
        wall, route = 0.5, 0
        src, dst = (random.randrange(w), random.randrange(h)), (random.randrange(w), random.randrange(h))
        if np.abs(src[0] - dst[0]) + np.abs(src[1] - dst[1]) < 100:
            continue
        if maze[src[1], src[0]] <= wall and maze[dst[1], dst[0]] <= wall:
            break
    path = dynamic_programming(maze, src, dst)
    #
    maze = maze > skimage.filters.threshold_mean(maze)
    maze = skimage.morphology.erosion(maze, selem=skimage.morphology.square(7))
    maze = skimage.filters.gaussian(maze)
    plt.imshow(maze, cmap='Greys')
    plt.show()
    draw_path(maze, path)
    #
    for idx, pt in enumerate(path):
        # sliding_window(maze, pt)
        rotate_window(maze, pt, 3.14 * idx * 0.1)


def main_2():
    # generate binary maze
    w, h = 21, 21
    maze_binary = make_maze(w, h)
    #
    w, h = 240, 240
    maze = skimage.transform.resize(maze_binary, (h, w), mode='edge')
    maze_binary_big = maze > skimage.filters.threshold_mean(maze)
    maze_for_dp = skimage.morphology.dilation(maze_binary_big, skimage.morphology.square(7))
    # dynamic_programming(maze_for_dp, ())
    #
    #
    plt.imshow(maze, cmap='Greys')
    plt.show()


if __name__ == '__main__':
    main_1()
    # main_2()
