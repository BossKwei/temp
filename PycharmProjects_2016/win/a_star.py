WIDTH = 16
HEIGHT = 8
MAX = 0xFF


m = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]


def find_neighbors(grid, point):
    dof = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    l = []
    for (du, dv) in dof:
        u = point[0] + du
        v = point[1] + dv
        if u in range(HEIGHT) and v in range(WIDTH):
            l.append((u, v))
    return l


def h_manhattan(src, dst):
    return abs(src[0]-dst[0]) + abs(src[1]-dst[1])


def mark_as_visited(grid, point):
    grid[point[0]][point[1]] = '-'


def mark_as_path(grid, point):
    grid[point[0]][point[1]] = 'X'


def point_is_valid(grid, point):
    if 'W' == grid[point[0]][point[1]]:
        return False
    else:
        return True


def search(grid, src, dst, visited=[], g={}, h={}, f={}, path={}):
    """
    :param grid:
    :param src:
    :param dst:
    :param visited:
    :param g: the distance between current point and start point
    :param h: the Manhattan distance between current point and end point
    :param f: f(x) = g(x) + h(x), in final release, this should be re-write of binary heap
    :param path: {'vertex_a', 'vertex_b'}, the way to vertex_a must through vertex_b
    :return:
    """
    if src == dst:
        step = dst
        while step is not None:
            mark_as_path(grid, step)
            step = path.get(step)
        #
        for i in range(HEIGHT):
            print(grid[i])
    else:
        if not visited:
            g[src] = 0
        # visit the neighbors
        for neighbor in find_neighbors(grid, src):
            if neighbor not in visited and point_is_valid(grid, neighbor):
                g[neighbor] = g[src] + 1
                h[neighbor] = h_manhattan(neighbor, dst)
                # if edges between vertexes are equal,
                # we could just update f[neighbor] without comparing new_f and old_f
                new_f = g[neighbor] + h[neighbor]
                if neighbor in f:
                    f[neighbor] = new_f if new_f < f[neighbor] else f[neighbor]
                else:
                    f[neighbor] = new_f
                path[neighbor] = src
                #
                mark_as_visited(grid, neighbor)
        # mark as visited
        visited.append(src)
        #
        x = min(f, key=f.get)
        f.pop(x)
        #
        search(grid, x, dst, visited, g, h, f)


if __name__ == '__main__':
    # search(m, (3, 3), (7, 14))
    # search(m, (3, 9), (7, 14))
    search(m, (7, 14), (3, 9))
