import random
import queue
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


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


def dynamic_programming(maze, src, dst):
    wall, route = 255, 0
    h, w = maze.shape
    visited = np.zeros_like(maze, dtype=np.bool)
    trace = np.zeros([h, w, 2], dtype=np.uint32)
    schedule = queue.Queue()
    #
    schedule.put(src)
    while True:
        x, y = schedule.get()
        visited[y, x] = True
        if (x, y) == dst:
            break
        else:
            for xx, yy in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
                if 0 <= xx < w and 0 <= yy < h:
                    if visited[yy, xx]:
                        continue
                    if maze[yy, xx] == wall:
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
    return path


def sliding_window(maze, pt, window_size=(32, 32)):
    wall, route = 255, 0
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
    # print(v_top - top, h_slide - bottom + v_bottom, v_left - left, w_slide - right + v_right)
    # a = maze[v_top:v_bottom, v_left:v_right]
    sw[v_top - top:h_slide - bottom + v_bottom, v_left - left:w_slide - right + v_right] = maze[v_top:v_bottom, v_left:v_right]
    # a = 1
    plt.imshow(sw, cmap='Greys')
    plt.draw()
    plt.pause(0.1)


def animation(maze):
    h, w = maze.shape
    maze_rgb = np.zeros([h, w, 3], dtype=np.uint8)
    maze_rgb[:, :, 0] = maze
    maze_rgb[:, :, 1] = maze
    maze_rgb[:, :, 2] = maze


def main():
    # w, h = 321, 241
    w, h = 81, 61
    maze = make_maze(w, h)
    while True:
        wall, route = 255, 0
        src, dst = (random.randrange(w), random.randrange(h)), (random.randrange(w), random.randrange(h))
        if maze[src[1], src[0]] == route and maze[dst[1], dst[0]] == route:
            break
    path = dynamic_programming(maze, src, dst)
    path = np.flip(path, axis=0)
    for pt in path:
        sliding_window(maze, pt)


if __name__ == '__main__':
    try:
        for _ in range(100):
            main()
    except KeyboardInterrupt:
        pass
