import math
from typing import List, Callable, Union
from PriorityQueue import PriorityQueue

# TODO:
# add subgraphs
# have get_node_by_id to return None rather than -1

class Digraph:
    class Node:
        def __init__(self, id: int, val=None) -> None:
            self.id = id            
            self.neighbours = {}    # dictionary of k:v id:weight
            self.val = val

        def info(self) -> None:
            print(f"Node: {self.id}")

        def other_info(self, other_node_info: Callable) -> None:
            print(f"My id: {self.id}, calling: ")
            other_node_info()

        def add_edge(self, id: int, weight: int) -> None:
            self.neighbours[id] = weight

        def remove_edge(self, id):
            if id in self.neighbours:
                del self.neighbours[id]
                return True
            return False

        def get_unweighted_neighbours(self) -> List[int]:
            return [neighbour for neighbour in self.neighbours]

        def get_weighted_neighours(self) -> dict:
            return self.neighbours

        def print_neighbours(self) -> None:
            print("-----------------------")
            self.info()
            print("Neighbours:")
            for neighbour in self.neighbours:
                print(f"ID: {neighbour}, weight: {self.neighbours[neighbour]}")
            print("-----------------------")

        def get_weight(self, id) -> int:
            return self.neighbours[id]

        def __hash__(self):
            return hash(self.id)

        # def __eq__(self, other):
        #     return other.id == self.id
    
    def __init__(self, num_nodes: int = 1) -> None:
        self.node_id_counter = num_nodes
        # self.val_dictionary = {None: [x] for x in range(num_nodes)}
        self.nodes = {x: self.Node(x) for x in range(num_nodes)}
    
    # TODO
    # Update to return None if not found
    def get_node_by_id(self, id: int) -> Union[Node, int]:
        if id not in self.nodes:
            return -1
        return self.nodes[id]

    # I wonder if there should be a backing dictionary to connect values to IDs so get_node_by_val is O(1).
    def get_node_by_val(self, val):
        pass


    def print_nodes(self) -> None:
        for node in self.nodes:
            node.print_neighbours()
        
    # this implies maybe I should have a set or dict id:index for O(1) rather than O(n)
    def contains_id(self, id: int) -> bool:
        if id in self.nodes:
            return True
        return False

    # adds a new node to the backing dictionary
    # Should maybe have a class variable to assign IDs rather than None
    def add_node(self, id=None, val=None) -> bool:
        if id not in self.nodes:
            self.node_id_counter += 1
            self.nodes[id] = self.Node(id,val)
            # if val not in self.val_dictionary:
            #     self.val_dictionary[val] = []
            # self.val_dictionary[val].append(id)
            return True
        return False

    # Removes a node from the backing dictionary as well as all incident edges from neighbours
    def remove_node(self, id) -> bool:
        if id not in self.nodes:
            return False
        # if self.nodes[id].val in self.val_dictionary:
        #     self.val_dictionary[self.nodes[id].val].remove(id)
        del self.nodes[id]
        for node in self.nodes:
            if id in self.nodes[node].get_weighted_neighours():
                self.nodes[node].remove_edge(id)
        return True

    # adds a directed weighted edge from node1 to node2
    def add_edge(self, node1: int, node2: int, weight: int) -> bool:
        if node1 not in self.nodes or node2 not in self.nodes:
            return False
        self.get_node_by_id(node1).add_edge(node2, weight)
        return True
    
    # not strictly necessary because the edges are stored in dictionaries, but reasonable to have
    def update_edge(self, updated_edge: List[int]) -> None:
        self.add_edge(updated_edge)

    def get_path_weight(self, path: List[List[int]]) -> int:
        total_weight = 0
        for i in range(1, len(path)):
            total_weight += self.get_node_by_id(path[i]).get_weight(path[i - 1])
        return total_weight

    def print_path(self, end: int, path_dict: dict) -> List[int]:
        path = [end]
        curr = path_dict[end]
        while curr is not None:
            path.append(curr)
            curr = path_dict[curr]
        print(f"{path[::-1 ]}, Weight: {self.get_path_weight(path)}")
        return path[::-1]

    # this was made redundant with the addition of first_search below
    def bfs(self, start: int, end: int) -> None:
        if self.get_node_by_id(start) == -1 or self.get_node_by_id(end) == -1:
            if self.get_node_by_id(start) == -1 and self.get_nod_by_id(end) == -1:
                print("Neither nodes exist.")
            elif self.get_node_by_id(start) == -1:
                print("Start node does not exist.")
            else:
                print("End node does not exist.")
            return
        print(f"Beginning BFS from {start} to {end}")
        queue = [start]
        seen = set()
        seen.add(start)
        path = {}
        path[start] = None
        while queue:
            curr = queue.pop(0)
            for neighbour in self.get_node_by_id(curr).get_unweighted_neighbours():
                if neighbour not in seen:
                    path[neighbour] = curr
                    if neighbour == end:
                        print(f"Reached {end}")
                        self.print_path(end, path)
                        return
                    seen.add(neighbour)
                    queue.append(neighbour)
        print("Unreachable.")

    # Makes sure both node1 and node2 exist
    def check_nodes_exist(self, node1: int, node2: int) -> bool:
        if self.get_node_by_id(node1) == -1 or self.get_node_by_id(node2) == -1:
            if self.get_node_by_id(node1) == -1 and self.get_node_by_id(node2) == -1:
                print("Neither nodes exist.")
            elif self.get_node_by_id(node1) == -1:
                print("Start node does not exist.")
            else:
                print("End node does not exist.")
            return False
        return True

    # why not, right? provide BFS = True parameter otherwise it'll DFS. Could probably return the path?
    def first_search(self, start: int, end: int, BFS: bool=False) -> List[int]:
        if not self.check_nodes_exist(start, end):
            return []
        if start == end:
            return [start]
        print(f"Beginning {'BFS' if BFS else 'DFS'} from {start} to {end}")
        queue = [start]
        seen = set()
        seen.add(start)
        path = {}
        path[start] = None
        while queue:
            curr = queue.pop(0) if BFS else queue.pop()
            for neighbour in self.get_node_by_id(curr).get_unweighted_neighbours():
                if neighbour not in seen:
                    path[neighbour] = curr
                    if neighbour == end:
                        print(f"Reached {end}")
                        return self.print_path(end, path)
                    seen.add(neighbour)
                    queue.append(neighbour)
        print("Unreachable.")
        return []


    # returns an adjacency matrix for the graph
    def get_path_matrix(self) -> List[List[int]]:
        paths = [[math.inf for x in range(len(self.nodes))] for y in range(len(self.nodes))]
        for i,node in enumerate(self.nodes):
            paths[i][i] = 0
            for key in self.nodes[node].get_weighted_neighours():
                paths[i][key] = self.nodes[node].get_weight(key)
        return paths

    # returns an adjacency matrix with all pairs shortest paths
    def floyd_warshall(self) -> List[List[int]]:
        paths = self.get_path_matrix()
        for k in range(len(paths)):
            for j in range(len(paths)):
                for i in range(len(paths)):
                    paths[i][j] = min([paths[i][k] + paths[k][j], paths[i][j]])
        return paths

    # prints then returns an adjacency matrix with all pairs shortest paths
    def apsp(self) -> None:
        paths = self.floyd_warshall()
        for i, path in enumerate(paths):
            print(f"{i}: {path}")
        return paths

    # probably doesn't actually need to take an end ID, will just return a list of single-source
    # shortest path from the start node
    def dijkstra(self, start: int, end: int) -> List[int]:
        if not self.check_nodes_exist(start, end):
            return []
        print(f"Beginning Dijkstra's algorithm from {start} to {end}.")
        pq = PriorityQueue()
        dist = {start: 0}
        prev = {start: None}

        for node in self.nodes:
            if self.nodes[node].id != start:
                dist[self.nodes[node].id] = math.inf
                prev[self.nodes[node].id] = None
            pq.add(self.nodes[node].id, dist[self.nodes[node].id])

        while not pq.is_empty():
            curr = pq.get_min()
            neighbours = self.get_node_by_id(curr).get_weighted_neighours()
            for neighbour in neighbours:
                alt = dist[curr] + neighbours[neighbour]
                if alt < dist[neighbour] and dist[curr] is not math.inf and pq.contains(neighbour):
                    dist[neighbour] = alt
                    prev[neighbour] = curr
                    pq.decrease_key(neighbour, alt)
        return self.print_path(end, prev)


    # uses prim's algorithm to return a dict with k:v parent:child for a minimum spanning tree
    # should maybe return a subgraph instead?
    def mst(self, start: int = 0) -> dict:
        print(f"Beginning Prim's algorithm from {start}")
        curr = self.get_node_by_id(start)
        pq = PriorityQueue()
        seen = set([start])
        unseen = set([self.nodes[x].id for x in self.nodes])
        unseen.remove(start)
        edge_dict = {}
        for edge in curr.get_weighted_neighours():
            pq.add(edge, curr.get_weighted_neighours()[edge])
            edge_dict[edge] = start
        while not pq.is_empty():
            node = pq.get_min()
            seen.add(node)
            for neighbour in self.get_node_by_id(node).get_weighted_neighours():
                if neighbour not in seen:
                    if not pq.contains(neighbour):
                        pq.add(neighbour, self.get_node_by_id(node).get_weighted_neighours()[neighbour])
                        edge_dict[neighbour] = node
                    else:
                        if self.get_node_by_id(node).get_weighted_neighours()[neighbour] < pq.get_weight(neighbour):
                            pq.decrease_key(neighbour, self.get_node_by_id(node).get_weighted_neighours()[neighbour])
                            edge_dict[neighbour] = node
        return edge_dict


class Graph(Digraph):
    def __init__(self, num_nodes: int = 1) -> None:
        super().__init__(num_nodes)

    def add_edge(self, node1: int, node2: int, weight: int) -> bool:
        if node1 not in self.nodes or node2 not in self.nodes:
            return False
        self.get_node_by_id(node1).add_edge(node2, weight)
        self.get_node_by_id(node2).add_edge(node1, weight)
        return True

    def remove_node(self, id) -> bool:
        if id not in self.nodes:
            return False
        for neighbour in self.get_node_by_id(id).get_weighted_neighours():
            self.nodes[neighbour].remove_edge(id)
        del self.nodes[id]
        return True


if __name__ == "__main__":
    network = Graph()
