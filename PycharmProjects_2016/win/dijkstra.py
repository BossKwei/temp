def dijkstra(graph, src, dst, visited=[], distances={}, way_must_be_passed={}):
    """
    :param graph:
    :param src:
    :param dst:
    :param visited: CLOSE
    :param distances: {'vertex', distance}, the minimum distance from vertex to initial src
    :param way_must_be_passed: {'vertex_a', 'vertex_b'}, the way to vertex_a must through vertex_b
    :return:
    """
    if src == dst:
        # we build the shortest path and display it
        path = []
        step = dst
        while step is not None:
            path.append(step)
            step = way_must_be_passed.get(step)
        print('shortest path:', path, ', cost:', distances[dst])
        print(way_must_be_passed)
    else:
        # if it is the initial run, initializes the cost
        if not visited:
            distances[src] = 0
        # visit the neighbors
        for neighbor in graph[src]:
            if neighbor not in visited:
                new_distance = distances[src] + graph[src][neighbor]
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    way_must_be_passed[neighbor] = src
        # mark as visited
        visited.append(src)
        # run Dijkstra with new src='x'
        unvisited = {}
        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k, float('inf'))
        x = min(unvisited, key=unvisited.get)
        dijkstra(graph, x, dst, visited, distances, way_must_be_passed)

"""
(f)  9  (e)   6  (d)
     2       11
14      (c)      15
     9       10
(a)      7       (b)
"""
if __name__ == "__main__":
    g = {'a': {'b': 7, 'c': 9, 'f': 14},
         'b': {'a': 7, 'c': 10, 'd': 15},
         'c': {'a': 9, 'b': 10, 'd': 11, 'f': 2},
         'd': {'b': 15, 'c': 11, 'e': 6},
         'e': {'d': 6, 'f': 9},
         'f': {'a': 14, 'c': 2, 'e': 9}}
    dijkstra(g, 'a', 'e')
