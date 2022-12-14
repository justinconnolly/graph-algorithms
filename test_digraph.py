import unittest
import Graph
import math

class GraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.edge_list = [
            [0,1,1],
            [0,3,3],
            [1,2,3],
            [1,3,1],
            [2,4,2],
            [2,5,5],
            [3,2,1],
            [3,4,4],
            [4,5,2],
            [4,1,2],
            [5,2,4]
        ]

        self.start_end = [
            [0,5],
            [5,1],
            [0,0],
            [1,6],
            [-1,5]
        ]

        self.solutions = {
            'bfs': [
                [0, 1, 2, 5],
                [5, 2, 4, 1],
                [0],
                [],
                []
            ],
            'dfs': [
                [0, 3, 4, 5],
                [5, 2, 4, 1],
                [0],
                [],
                []
            ],
            'dijkstra': [
                [0, 1, 3, 2, 4, 5],
                [5, 2, 4, 1],
                [0],
                [],
                []      
            ],
            'mst': {
                1: 0, 2: 3, 3: 1, 4: 2, 5: 4
            },

            'apsp': [
                [0, 1, 3, 2, 5, 7],
                [math.inf, 0, 2, 1, 4, 6],
                [math.inf, 4, 0, 5, 2, 4],
                [math.inf, 5, 1, 0, 3, 5],
                [math.inf, 2, 4, 3, 0, 2],
                [math.inf, 8, 4, 9, 6, 0]
            ]
        }
        self.graph = Graph.Digraph(6)
        for edge in self.edge_list:
            self.graph.add_edge(edge[0], edge[1], edge[2])

    

    def bfs_test(self, i):
        self.assertEqual(self.graph.first_search(self.start_end[i][0],self.start_end[i][1], True), self.solutions['bfs'][i])

    def dfs_test(self, i):
        self.assertEqual(self.graph.first_search(self.start_end[i][0],self.start_end[i][1], False), self.solutions['dfs'][i])
    
    def dijkstra_test(self, i):
        self.assertEqual(self.graph.dijkstra(self.start_end[i][0],self.start_end[i][1]), self.solutions['dijkstra'][i])

       
    def test_paths(self):
        for i, v in enumerate(self.start_end):
            self.bfs_test(i)
            self.dfs_test(i)
            self.dijkstra_test(i)

    def test_MST(self):
        self.assertEqual(self.graph.mst(), self.solutions['mst'])

    def test_APSP(self):
        self.assertEqual(self.graph.apsp(), self.solutions['apsp'])

    def test_add_remove(self):
        self.assertTrue(self.graph.remove_node(1))
        self.assertFalse(self.graph.contains_id(1))
        self.assertFalse(self.graph.remove_node(1))
        self.assertTrue(self.graph.add_node(1))
        self.assertTrue(self.graph.contains_id(1))
        self.assertFalse(self.graph.add_node(1))
        self.assertTrue(self.graph.add_edge(0,1,1))
        self.assertTrue(self.graph.add_edge(1,2,3))
        self.assertTrue(self.graph.add_edge(1,3,1))
        self.assertTrue(self.graph.add_node('String'))
        self.assertTrue(self.graph.add_edge('String', 1, 5))


if __name__ == "__main__":
    unittest.main()