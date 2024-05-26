import unittest
from assign_rooms import assign_rooms_to_exams
from build_conflict_graph import build_conflict_graph
from welsh_powell_coloring import welsh_powell_coloring

class TestAssignRoomsToExams(unittest.TestCase):
    def setUp(self):
        self.exams = [
            {"id": 1, "name": "Math", "students": [1, 2, 3], "duration": 2},
            {"id": 2, "name": "Physics", "students": [1, 3, 4], "duration": 1},
            {"id": 3, "name": "Chemistry", "students": [2, 4, 5], "duration": 2},
            {"id": 4, "name": "Biology", "students": [1, 2, 5], "duration": 1},
            {"id": 5, "name": "History", "students": [3, 4, 5], "duration": 1}
        ]
        self.rooms = [
            {"id": 1, "capacity": 4},
            {"id": 2, "capacity": 3}
        ]
        self.time_slots = [
            {"id": 1, "start": "09:00", "end": "11:00", "duration": 2},
            {"id": 2, "start": "12:00", "end": "13:00", "duration": 1},
            {"id": 3, "start": "14:00", "end": "15:00", "duration": 1},
            {"id": 99, "start": "non_programmed", "end": "non_programmed", "duration": float('inf')}
        ]
        self.G = build_conflict_graph(self.exams)
        self.coloring = welsh_powell_coloring(self.G)

    def test_assign_rooms_to_exams(self):
        schedule, penalty_schedule = assign_rooms_to_exams(self.coloring, self.exams, self.rooms, self.time_slots)
        # Verifier que les examens sont assignés sans redundance
        print("Vérification que les examens sont assignés sans redondance...")
        self.assertEqual(sum(len(slot) for slot in schedule.values()), len(self.exams))
        
        # Verifier que les examens sont assignés dans des salles de capacité suffisante
        print("Vérification que les examens sont assignés dans des salles de capacité suffisante...")
        self.assertTrue(all(len(room['exam']['students']) <= self.rooms[room['room'] - 1]['capacity']
                            for slot in schedule.values() for room in slot))
if __name__ == '__main__':
    unittest.main()
