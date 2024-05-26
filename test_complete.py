import unittest
from test_build_conflict_graph import TestBuildConflictGraph
from test_assign_rooms import TestAssignRoomsToExams
from test_coloring import TestWelshPowellColoring

# Utilities
from utils import *
import glob

class TestComplete(unittest.TestCase):
    def setUp(self):
        test_folders = glob.glob("test[1-9]*")
        ##
        print(f"loading {len(test_folders)} test folders:", *test_folders)
        #
        self.test_cases = [load_test(folder) for folder in test_folders]

    def testComplete(self):
        for i in range(1, len(self.test_cases)+1):
            print(f"\nDebut du test {i}. Dossier ./test{i}")
            print("\t1. Chargement des données ...", end="\t")
            exams, students, time_slots, rooms, room_slots = self.test_cases[i-1]
            print("OK")
            # Creation du graphe de conflit
            print("\t2. Création du graphe de conflite ...", end="\t")
            G = build_conflict_graph(exams)
            print("OK")
            print("\t3. Coloration avec l'algorihme de Welsh-Powell", end="\t")
            coloring = welsh_powell_coloring(G)
            print("OK")
            utime_slots = time_slots if any(slot['id'] == 99 for slot in time_slots) else time_slots + [{"id": 99, "start": "non_programmé", "end": "non_programmé", "duration": float("inf")}]
            print("\t4. Assignation des salles d'examens ...", end="\t")
            schedule, penalty_schedule = assign_rooms_to_exams(coloring, exams, rooms, utime_slots)
            print("OK")
            print("\t5. Amélioratoin de la solution optimale ...", end="\t")
            improved_schedule, improved_penalty_schedule = local_search_improvement(schedule, exams, rooms, time_slots, penalty_schedule, 1000)
            print("OK")

            # Checks
            print(f"Debut de vérification des contraintes pour le test {i}")
            print("\t1. Check de contraintes de non conflits dans la programmation ...", end="\t")
            self.assertEqual(anyerror_exams_conflicts(improved_schedule, exams), 0)
            print("OK")
            print("\t2. Check de contraintes de capacté pour les salles ...", end="\t")
            self.assertEqual(anyerror_room_capacities(schedule, rooms), 0)
            print("OK")
            break

            print(f"---- Test {i} terminé avec succès ----")

if __name__ == "__main__":
    unittest.main()
    