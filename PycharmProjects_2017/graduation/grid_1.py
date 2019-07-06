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
        if visited[y, x]:
            continue
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


def draw_path(maze, path):
    wall, route = 255, 0
    canvas = np.copy(maze)
    for x, y in path:
        canvas[y, x] = (wall + route) // 2
    plt.imshow(canvas, cmap='Greys')
    plt.draw()
    plt.pause(0.1)


def main():
    maze = None
    try:
        w, h = 161, 121
        wall, route = 255, 0
        for _ in tqdm(range(100)):
            maze = make_maze(w, h)
            for _ in tqdm(range(1000)):
                while True:
                    src, dst = (random.randrange(w), random.randrange(h)), (random.randrange(w), random.randrange(h))
                    if maze[src[1], src[0]] == route and maze[dst[1], dst[0]] == route:
                        break
                path = dynamic_programming(maze, src, dst)
                assert len(path)
                draw_path(maze, path)
    except Exception as e:
        print(e)
        print(maze)


if __name__ == '__main__':
    main()
