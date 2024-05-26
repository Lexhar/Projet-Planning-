import unittest
from utils import build_conflict_graph, welsh_powell_coloring

class TestWelshPowellColoring(unittest.TestCase):
    def setUp(self):
        self.exams = [
            {"id": 1, "name": "Math", "students": [1, 2, 3], "duration": 2},
            {"id": 2, "name": "Physics", "students": [1, 3, 4], "duration": 1},
            {"id": 3, "name": "Chemistry", "students": [2, 4, 5], "duration": 2},
            {"id": 4, "name": "Biology", "students": [1, 2, 5], "duration": 1},
            {"id": 5, "name": "History", "students": [3, 4, 5], "duration": 1}
        ]
        self.G = build_conflict_graph(self.exams)

    def test_welsh_powell_coloring(self):
        # print test name
        print("Running", self._testMethodName, "."*3)

        # start testing
        coloring = welsh_powell_coloring(self.G)
        self.assertEqual(len(coloring), len(self.exams))
        self.assertNotEqual(coloring[1], coloring[2])
        self.assertNotEqual(coloring[2], coloring[3])

if __name__ == '__main__':
    unittest.main()
