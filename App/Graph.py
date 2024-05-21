from collections import deque
import heapq

class Graph:
    def __init__(self, directed=True):
        self.vertices = {}
        self.directed = directed
    
    def add_vertex(self, vertex: str) -> None:
        if vertex not in self.vertices:
            self.vertices[vertex] = {}

    def has_vertex(self, vertex: str) -> bool:
        return vertex in self.vertices
    
    def add_edge(self, vertex1: str, vertex2: str, weight1: int, weight2: int) -> None:
        if vertex1 not in self.vertices:
            self.add_vertex(vertex1)
        if vertex2 not in self.vertices:
            self.add_vertex(vertex2)

        if vertex2 in self.vertices[vertex1]:
            if self.vertices[vertex1][vertex2][0] > weight1:
                self.vertices[vertex1][vertex2] = (weight1, weight2)
        else:
            self.vertices[vertex1][vertex2] = (weight1, weight2)

        if not self.directed:
            if vertex1 in self.vertices[vertex2]:
                if self.vertices[vertex2][vertex1][0] > weight1:
                    self.vertices[vertex2][vertex1] = (weight1, weight2)
            else:
                self.vertices[vertex2][vertex1] = (weight1, weight2)

    def get_vertices(self) -> list:
        return list(self.vertices.keys())
    
    def get_neighbors(self, vertex: str) -> dict:
        return self.vertices[vertex]

    def get_weight(self, vertex1: str, vertex2: str) -> tuple:
        if vertex1 in self.vertices and vertex2 in self.vertices[vertex1]:
            return self.vertices[vertex1][vertex2]
        else:
            return None
        
    def get_indegree(self, vertex: str) -> int:
        indegree = 0
        for v in self.vertices:
            if vertex in self.vertices[v]:
                indegree += 1
        return indegree

    def get_outdegree(self, vertex: str) -> int:
        if vertex in self.vertices:
            return len(self.vertices[vertex])
        else:
            return 0
        
    def get_degree(self, vertex: str) -> int:
        return self.get_indegree(vertex) + self.get_outdegree(vertex)
    
    #===========================================================================
    # ALGORITHMS
    #===========================================================================
    
    def bfs_path(self, start: str, goal: str) -> list:
        if start not in self.vertices or goal not in self.vertices:
            return []

        queue = deque([(start, [(start, (0, 0))])])
        visited = set()

        while queue:
            vertex, path = queue.popleft()
            if vertex in visited:
                continue

            for next_vertex, (weight1, weight2) in self.get_neighbors(vertex).items():
                if next_vertex in visited:
                    continue
                if next_vertex == goal:
                    return path + [(next_vertex, (weight1, weight2))]
                else:
                    queue.append((next_vertex, path + [(next_vertex, (weight1, weight2))]))

            visited.add(vertex)

        return []

    def has_path(self, start: str, goal: str) -> bool:
        return bool(self.bfs_path(start, goal))

    def prim(self, start_vertex: str):
        if start_vertex not in self.vertices:
            raise ValueError("El vértice inicial no está en el grafo.")

        mst = Graph(directed=self.directed)
        mst.add_vertex(start_vertex)

        visited = set()
        visited.add(start_vertex)

        edges = [
            (weight1, weight2, start_vertex, neighbor) 
            for neighbor, (weight1, weight2) in self.get_neighbors(start_vertex).items()
        ]
        heapq.heapify(edges)

        total_cost_weight1 = 0
        total_cost_weight2 = 0

        while edges:
            weight1, weight2, vertex1, vertex2 = heapq.heappop(edges)

            if vertex2 not in visited:
                visited.add(vertex2)
                mst.add_vertex(vertex2)
                mst.add_edge(vertex1, vertex2, weight1, weight2)
                total_cost_weight1 += weight1
                total_cost_weight2 += weight2

                for next_neighbor, (next_weight1, next_weight2) in self.get_neighbors(vertex2).items():
                    if next_neighbor not in visited:
                        heapq.heappush(edges, (next_weight1, next_weight2, vertex2, next_neighbor))

        return mst, total_cost_weight1, total_cost_weight2

    def find_branches(self, start_vertex):
        def dfs(vertex, path, visited):
            if path:
                last_vertex, last_weights = path[-1]
                path.append((vertex, self.get_weight(last_vertex, vertex)))
            else:
                path.append((vertex, (0, 0)))
            visited.add(vertex)

            neighbors = self.get_neighbors(vertex)
            if len(neighbors) == 0 or all(neighbor in visited for neighbor in neighbors):
                branches.append(list(path))
            else:
                for neighbor in neighbors:
                    if neighbor not in visited:
                        dfs(neighbor, path, visited)

            path.pop()
            visited.remove(vertex)

        branches = []
        if start_vertex in self.vertices:
            dfs(start_vertex, [], set())
        return branches
    
    def dijkstra(self, start: str, end: str):
            if start not in self.vertices or end not in self.vertices:
                raise ValueError("Los vértices inicial y/o final no están en el grafo.")

            distances = {vertex: float('inf') for vertex in self.vertices}
            distances[start] = 0
            previous = {vertex: None for vertex in self.vertices}

            priority_queue = [(0, start)]
            heapq.heapify(priority_queue)

            while priority_queue:
                current_distance, current_vertex = heapq.heappop(priority_queue)

                if current_vertex == end:
                    break

                if current_distance > distances[current_vertex]:
                    continue

                for neighbor, (weight1, weight2) in self.get_neighbors(current_vertex).items():
                    distance = current_distance + weight2

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = (current_vertex, weight1, weight2)
                        heapq.heappush(priority_queue, (distance, neighbor))

            # Reconstruir el camino y calcular los costos
            path = []
            path_weights = []
            current = end
            while current is not None:
                if previous[current] is not None:
                    prev_vertex, weight1, weight2 = previous[current]
                    path.insert(0, current)
                    path_weights.insert(0, (weight1, weight2))
                    current = prev_vertex
                else:
                    path.insert(0, current)
                    current = None

            total_weight1 = sum(weight1 for weight1, weight2 in path_weights)
            total_weight2 = sum(weight2 for weight1, weight2 in path_weights)
            
            return path, path_weights, total_weight1, total_weight2
