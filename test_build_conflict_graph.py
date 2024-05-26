import unittest
import networkx as nx
from build_conflict_graph import build_conflict_graph

class TestBuildConflictGraph(unittest.TestCase):
    def setUp(self):
        # Test data
        self.exams = [
            {"id": 1, "name": "Math", "students": [1, 2, 3], "duration": 2},
            {"id": 2, "name": "Physics", "students": [1, 3, 4], "duration": 1},
            {"id": 3, "name": "Chemistry", "students": [2, 4, 5], "duration": 2},
            {"id": 4, "name": "Biology", "students": [1, 2, 5], "duration": 1},
            {"id": 5, "name": "History", "students": [4, 5], "duration": 1}
        ]

    def test_build_conflict_graph(self):
        # print test name
        print("Running", self._testMethodName, "."*3)

        # Start testing
        G = build_conflict_graph(self.exams)
        self.assertEqual(len(G.nodes), len(self.exams))
        self.assertTrue(G.has_edge(1, 2))
        self.assertTrue(G.has_edge(2, 3))
        self.assertFalse(G.has_edge(1, 5))

if __name__ == '__main__':
    unittest.main()
