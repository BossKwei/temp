import random
import queue
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def make_maze(w=81, h=61):
    wall, route = 255, 0
    maze = np.ones([h, w], dtype=np.uint8) * wall
    visited = np.zeros_like(maze, dtype=np.bool)

    def walk(x, y):
        maze[y][x] = route
        visited[y][x] = True
        neighbors = [(x, y - 2), (x, y + 2), (x - 2, y), (x + 2, y)]
        random.shuffle(neighbors)
        for xx, yy in neighbors:
            if 0 <= xx < w and 0 <= yy < h:
                if visited[yy, xx]:
                    continue
                if xx == x:
                    maze[(yy + y) // 2, xx] = route
                if yy == y:
                    maze[yy, (xx + x) // 2] = route
                walk(xx, yy)
    walk(1, 1)
    # plt.imshow(maze, cmap='Greys')
    # plt.show()
    return maze


def dynamic_programming_1(maze, src, dst):
    wall, route = 255, 0
    h, w = maze.shape
    visited = np.zeros_like(maze, dtype=np.bool)
    path = []

    def walk(x, y):
        visited[y][x] = True
        if (x, y) == dst:
            return True
        else:
            is_optimal = False
            for xx, yy in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
                if 0 <= xx < w and 0 <= yy < h:
                    if visited[yy, xx]:
                        continue
                    if maze[yy, xx] == wall:
                        continue
                    is_optimal = walk(xx, yy)
                    if is_optimal:
                        path.append((xx, yy))
                        break
            return is_optimal
    walk(src[0], src[1])
    return path


def dynamic_programming_2(maze, src, dst):
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


def draw_path(maze, path):
    wall, route = 255, 0
    canvas = np.copy(maze)
    for x, y in path:
        canvas[y, x] = (wall + route) // 2
    plt.imshow(canvas, cmap='Greys')
    plt.show()


def main():
    for i in tqdm(range(100000)):
        maze = make_maze(41, 31)
        path_1 = dynamic_programming_1(maze, (1, 1), (39, 29))
        path_2 = dynamic_programming_2(maze, (1, 1), (39, 29))
        error = np.sum(np.subtract(path_1, path_2))
        assert error == 0


if __name__ == '__main__':
    main()
