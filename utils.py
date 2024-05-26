import networkx as nx
import pandas as pd
import pulp
import os

# Construire le graph de conflits entre les examens
# Si deux examens partagent la même arrête elles sont incompatible
def build_conflict_graph(exams):
    G = nx.Graph()
    for exam in exams:
        G.add_node(exam['id'], students=exam['students'], duration=exam['duration'])
    for i, exam1 in enumerate(exams):
        for j, exam2 in enumerate(exams):
            intersection = set(exam1['students']).intersection(exam2['students'])
            if i < j and intersection:
                G.add_edge(exam1['id'], exam2['id'])
    return G

# Utiliser l'algorithme de Welsh-Powell pour ressortir une coloration du graphe
def welsh_powell_coloring(G):
    coloring = {}
    nodes = sorted(G.nodes(), key=lambda x: len(list(G.neighbors(x))), reverse=True)
    available_colors = 0
    for node in nodes:
        neighbor_colors = {coloring[neighbor] for neighbor in G.neighbors(node) if neighbor in coloring}
        for color in range(available_colors):
            if color not in neighbor_colors:
                coloring[node] = color
                break
        else:
            coloring[node] = available_colors
            available_colors += 1
    return coloring


# Assigner aux différentes salles les examens en prenant les capacités et les nombres d'étudiants en compte
# A la sortie nous avons une solution initiale réalisable
def assign_rooms_to_exams(coloring, exams, rooms, time_slots):
    time_slots = time_slots if any(slot["id"] for slot in time_slots if slot["id"]==99) else [{"id": 99, "start": "non_programmed", "end": "non_programmed", "duration": float("inf")}] + time_slots
    schedule = {slot['id']: [] for slot in time_slots}
    penalty_schedule = []
    for exam_id, color in coloring.items():
        exam = next(exam for exam in exams if exam['id'] == exam_id)
        time_slot_id = time_slots[color]['id'] if color < len(time_slots) else 99
        room_assigned = False
        for room in rooms:
            if len(exam['students']) <= room['capacity']:
                schedule[time_slot_id].append({'exam': exam, 'room': room['id']})
                room_assigned = True if time_slot_id != 99 else False
                break
        if not room_assigned:
            penalty_schedule.append(exam_id)
    return schedule, penalty_schedule

# Fonction pour se rassurer qu'une programmation respecte les contraintes
# de capacites de salles
def check_room_capacities(schedule, rooms):
    """Return the amount of errors: number of students in a room > capacity"""
    errors = 0
    for time_slot_id, exam_room in schedule.items():
        room_students = dict()
        if time_slot_id == 99:
            continue
        for item in exam_room:
            room_id = item['room']
            exam_students = len(item['exam']['students'])
            room_students[room_id] = room_students.get(room_id, 0) + exam_students
            if room_students[room_id] > next(room['capacity'] for room in rooms if room['id'] == room_id):
                errors += 1
    return errors

def anyerror_room_capacities(schedule, rooms):
    """Return the amount of errors: number of students in a room > capacity"""
    errors = 0
    for time_slot_id, exam_room in schedule.items():
        if time_slot_id == 99:
            continue
        room_students = dict()
        for item in exam_room:
            room_id = item['room']
            exam_students = len(item['exam']['students'])
            room_students[room_id] = room_students.get(room_id, 0) + exam_students
            if room_students[room_id] > next(room['capacity'] for room in rooms if room['id'] == room_id):
                errors += 1
                return True
    return errors

# de conflits d'etudiants
def check_exams_conflicts(schedule, exams):
    """Return the amount of errors: number of conflicting exams"""
    G = build_conflict_graph(exams)
    errors = 0
    for time_slot_id, item in schedule.items():
        if time_slot_id == 99:
            continue
        for i in range(len(item)):
            for j in range(i + 1, len(item)):
                exam1 = item[i]['exam']['id']
                exam2 = item[j]['exam']['id']
                if G.has_edge(exam1, exam2):
                    errors += 1
    return errors

# de conflits d'etudiants
def anyerror_exams_conflicts(schedule, exams):
    """Return the amount of errors: number of conflicting exams"""
    G = build_conflict_graph(exams)
    errors = 0
    for time_slot_id, item in schedule.items():
        if time_slot_id == 99:
            continue
        for i in range(len(item)):
            for j in range(i + 1, len(item)):
                exam1 = item[i]['exam']['id']
                exam2 = item[j]['exam']['id']
                if G.has_edge(exam1, exam2):
                    errors += 1
                    return True
    return errors

# La fonction coût que l'on cherche à minimiser
# L'algorithme cherche à minimiser le nombre d'examens non programmés
def calculate_cost(schedule, penalty_schedule, penalty, exams, rooms):
    check1 = check_exams_conflicts(schedule, exams)
    check1 = float("inf") if check1 > 0 else 0
    check2 = check_room_capacities(schedule, rooms)
    check2 = float("inf") if check2 > 0 else 0

    return len(penalty_schedule) * penalty + check1 + check2



# Fonction de recherche locale pour améliorer la solution initiale
# Elle essaie de trouver un meilleure solution, compare les coûts et garde la meilleure
def local_search_improvement(schedule, exams, rooms, time_slots, penalty_schedule, penalty):
    best_schedule = schedule.copy()
    best_penalty_schedule = penalty_schedule.copy()
    best_cost = calculate_cost(schedule, penalty_schedule, penalty, exams, rooms)
    
    for exam_id in penalty_schedule:
        exam = next(exam for exam in exams if exam['id'] == exam_id)
        for time_slot in time_slots:
            if time_slot['id'] == 99:
                continue
            for room in rooms:
                if room['capacity'] >= len(exam['students']):
                    new_schedule = {k: v.copy() for k, v in best_schedule.items()}
                    new_schedule[time_slot['id']].append({'exam': exam, 'room': room['id']})
                    # Enlève l'examen de la liste des examens non programmés
                    for schedule in new_schedule[99]:
                        if schedule['exam']['id'] == exam_id:
                            new_schedule[99].remove(schedule)
                    new_penalty_schedule = [e for e in best_penalty_schedule if e != exam_id]
                    new_cost = calculate_cost(new_schedule, new_penalty_schedule, penalty, exams, rooms)
                    # Vérifie si le nouveau coût est plus petit que le meilleur coût
                    if new_cost < best_cost:
                        best_schedule = new_schedule
                        best_penalty_schedule = new_penalty_schedule
                        best_cost = new_cost
    best_penalty_schedule = [sched["exam"]["id"] for sched in best_schedule.get(99, [])]
    print("Penalty Schedule: ", best_penalty_schedule)
    return best_schedule, best_penalty_schedule

# Tabu Search algorithm
def tabu_search(schedule, exams, rooms, time_slots, penalty_schedule, penalty, max_iterations=100, tabu_tenure=5):
    best_schedule = schedule.copy()
    best_penalty_schedule = penalty_schedule.copy()
    best_cost = calculate_cost(schedule, penalty_schedule, penalty, exams, rooms)
    
    tabu_list = []
    
    for iteration in range(max_iterations):
        neighborhood = []

        # Generate neighborhood solutions by trying to reschedule unscheduled exams
        for exam_id in penalty_schedule:
            exam = next(exam for exam in exams if exam['id'] == exam_id)
            for time_slot in time_slots:
                if time_slot['id'] == 99:
                    continue
                for room in rooms:
                    if room['capacity'] >= len(exam['students']):
                        new_schedule = {k: v.copy() for k, v in best_schedule.items()}
                        if time_slot['id'] not in new_schedule:
                            new_schedule[time_slot['id']] = []
                        new_schedule[time_slot['id']].append({'exam': exam, 'room': room['id']})
                        new_penalty_schedule = [e for e in best_penalty_schedule if e != exam_id]
                        new_cost = calculate_cost(new_schedule, new_penalty_schedule, penalty, exams, rooms)
                        neighborhood.append((new_schedule, new_penalty_schedule, new_cost, (exam_id, time_slot['id'], room['id'])))
        
        # Select the best neighbor solution not in tabu list
        neighborhood = sorted(neighborhood, key=lambda x: x[2])
        for neighbor in neighborhood:
            if neighbor[3] not in tabu_list:
                best_schedule, best_penalty_schedule, best_cost = neighbor[0], neighbor[1], neighbor[2]
                tabu_list.append(neighbor[3])
                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)
                break
    best_penalty_schedule = [sched["exam"]["id"] for sched in best_schedule.get(99, [])]
    return best_schedule, best_penalty_schedule

def run_local_method(exams, time_slots, rooms):
    print("Planning avec optimisation locale")
    # Construire le graphe des conflits
    G = build_conflict_graph(exams)
    # Appliquer l'algorithme de Welsh-Powell
    coloring = welsh_powell_coloring(G)
    print("Coloration: ", coloring, end="\n\n")

    utime_slots = time_slots if any(slot['id'] == 99 for slot in time_slots) else time_slots + [{"id": 99, "start": "non_programmé", "end": "non_programmé", "duration": float("inf")}]

    # Assigner les salles aux examens
    print("Assignation des salles et plages")
    schedule, penalty_schedule = assign_rooms_to_exams(coloring, exams, rooms, utime_slots)

    # Afficher le planning initial
    print("\nSchedule : ")
    print(*schedule.items(), sep="\n", end="\n\n")
    print(penalty_schedule, end="\n\n")

    # Améliorer la solution initiale par recherche locale
    improved_schedule, improved_penalty_schedule = local_search_improvement(schedule, exams, rooms, time_slots, penalty_schedule, 1000)
    print("Improved Schedule : ")
    print(*improved_schedule.items(), sep="\n", end="\n\n")
    print("Improved Penalty : ", improved_penalty_schedule)


    # Afficher le planning amélioré
    for time_slot, scheduled_exams in improved_schedule.items():
        if time_slot == 99:
            print(f"Time Slot {time_slot} (non-programmed with penalty):")
            for item in scheduled_exams:
                print(f"\t{item['exam']['name']} is not scheduled.")
        else:
            print(f"Time Slot {time_slot}:")
            for item in scheduled_exams:
                exam = item['exam']
                room = item['room']
                print(f"\t{exam['name']} in Room {room}")

    total_penalty = calculate_cost(improved_schedule, improved_penalty_schedule, 1000, exams, rooms)
    print(f"Total penalty for non-programmed exams: {total_penalty}")
    return improved_schedule

# Tabu Search algorithm
def tabu_search(schedule, exams, rooms, time_slots, penalty_schedule, penalty, max_iterations=100, tabu_tenure=5):
    best_schedule = schedule.copy()
    best_penalty_schedule = penalty_schedule.copy()
    best_cost = calculate_cost(schedule, penalty_schedule, penalty, exams, rooms)
    
    tabu_list = []
    
    for iteration in range(max_iterations):
        neighborhood = []

        # Generate neighborhood solutions by trying to reschedule unscheduled exams
        for exam_id in penalty_schedule:
            exam = next(exam for exam in exams if exam['id'] == exam_id)
            for time_slot in time_slots:
                if time_slot['id'] == 99:
                    continue
                for room in rooms:
                    if room['capacity'] >= len(exam['students']):
                        new_schedule = {k: v.copy() for k, v in best_schedule.items()}
                        if time_slot['id'] not in new_schedule:
                            new_schedule[time_slot['id']] = []
                        new_schedule[time_slot['id']].append({'exam': exam, 'room': room['id']})
                        new_penalty_schedule = [e for e in best_penalty_schedule if e != exam_id]
                        new_cost = calculate_cost(new_schedule, new_penalty_schedule, penalty, exams, rooms)
                        neighborhood.append((new_schedule, new_penalty_schedule, new_cost, (exam_id, time_slot['id'], room['id'])))
        
        # Select the best neighbor solution not in tabu list
        neighborhood = sorted(neighborhood, key=lambda x: x[2])
        for neighbor in neighborhood:
            if neighbor[3] not in tabu_list:
                best_schedule, best_penalty_schedule, best_cost = neighbor[0], neighbor[1], neighbor[2]
                tabu_list.append(neighbor[3])
                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)
                break
    best_penalty_schedule = [sched["exam"]["id"] for sched in best_schedule.get(99, [])]
    return best_schedule, best_penalty_schedule

def run_tabu_method(exams, time_slots, rooms):
    # Initial setup
    G = build_conflict_graph(exams)
    coloring = welsh_powell_coloring(G)
    utime_slots = time_slots if any(slot["id"] for slot in time_slots if slot["id"]==99) else [{"id": 99, "start": "non_programmed", "end": "non_programmed", "duration": float("inf")}] + time_slots
    schedule, penalty_schedule = tabu_assign_rooms_to_exams(coloring, exams, rooms, utime_slots)
    print(*schedule.items(), sep="\n", end="\n\n")
    # Apply Tabu Search to improve the schedule
    improved_schedule, improved_penalty_schedule = tabu_search(schedule, exams, rooms, time_slots, penalty_schedule, 1000)
    print(improved_schedule)

    # Display the improved schedule
    for time_slot, scheduled_exams in improved_schedule.items():
        if time_slot == 99:
            print(f"Time Slot {time_slot} (non-programmed with penalty):")
            for exam_id in improved_penalty_schedule:
                print(f"  Exam {exams[exam_id - 1]['name']} is not scheduled.")
        else:
            print(f"Time Slot {time_slot}:")
            for item in scheduled_exams:
                exam = item['exam']
                room = item['room']
                print(f"  Exam {exam['name']} in Room {room}")

    total_penalty = calculate_cost(improved_schedule, improved_penalty_schedule, 1000, exams, rooms)
    print(f"Total penalty for non-programmed exams: {total_penalty}")

def create_test_case(number_of_exams = 3, number_of_students = 5, number_of_rooms = 3, number_of_time_slots = 3):
    import random
    
    # Generate exam data
    exams = []
    for i in range(1, number_of_exams + 1):
        exam = {
            "id": i,
            "name": f"Exam {i}",
            "students": random.sample(range(1, number_of_students + 1), random.randint(10, 30)),
            "duration": random.randint(1, 3)
        }
        exams.append(exam)

    # Generate student data
    students = []
    for i in range(1, number_of_students + 1):
        student = {
            "id": i,
            "name": f"Student {i}",
            "promotion": random.randint(1, 4)
        }
        students.append(student)

    # Generate room data
    rooms = []
    for i in range(1, number_of_rooms + 1):
        room = {
            "id": i,
            "capacity": random.randint(10, 30)
        }
        rooms.append(room)

    # Generate time slot data
    time_slots = []
    for i in range(1, number_of_time_slots + 1):
        time_slot = {
            "id": i,
            "start": f"2022-01-01 {random.randint(8, 16)}:00",
            "end": f"2022-01-01 {random.randint(17, 23)}:00",
            "duration": random.randint(1, 4)
        }
        time_slots.append(time_slot)
    
    return exams, students, rooms, time_slots

# Save the data in a folder
def save_test(folder_path, exams, students, time_slots, rooms):
    if not os.path.exists(folder_path):
        # Create target Directory
        os.mkdir(folder_path)
        print("Directory ", folder_path, " Created ")
    # save all the data
    pd.DataFrame(exams).to_csv(folder_path + "/exams.csv", index=False)
    pd.DataFrame(students).to_csv(folder_path + "/students.csv", index=False)
    pd.DataFrame(time_slots).to_csv(folder_path + "/time_slots.csv", index=False)
    pd.DataFrame(rooms).to_csv(folder_path + "/rooms.csv", index=False)
    print("All files saved in ", folder_path)

def load_test(folder_path):
    exams = pd.read_csv(folder_path + "/exams.csv").to_dict(orient="records")
    students = pd.read_csv(folder_path + "/students.csv").to_dict(orient="records")
    time_slots = pd.read_csv(folder_path + "/time_slots.csv").to_dict(orient="records")
    rooms = pd.read_csv(folder_path + "/rooms.csv").to_dict(orient="records")
    
    for exam in exams:
        exam["students"] = txt_to_list(exam["students"])
    # Generate room_slots
    room_slots = {}
    idDesignation = 1
    for room in rooms:
        for time_slot in time_slots:
            room_slots[idDesignation] = (room["id"], time_slot["id"])
            idDesignation += 1
    return exams, students, time_slots, rooms, room_slots

# tabu : Assign rooms to exams based on initial coloring
def tabu_assign_rooms_to_exams(coloring, exams, rooms, time_slots):
    schedule = {slot['id']: [] for slot in time_slots}
    penalty_schedule = []
    for exam_id, color in coloring.items():
        exam = next(exam for exam in exams if exam['id'] == exam_id)
        if color < len(time_slots):
            time_slot_id = time_slots[color]['id']
        else:
            time_slot_id = 99
        room_assigned = False
        for room in rooms:
            if len(exam['students']) <= room['capacity']:
                schedule[time_slot_id].append({'exam': exam, 'room': room['id']})
                room_assigned = True
                break
        if not room_assigned:
            penalty_schedule.append(exam_id)
    return schedule, penalty_schedule

def txt_to_list(txt):
    txt = txt[1:-1]
    return [int(nbr.strip()) for nbr in txt.split(",") ]
def col_to_nodes(coloring):
    dico = dict()
    for k, v in coloring.items():
        if v in dico:
            dico[v].append(k)
        else:
            dico[v] = [k]
    return dico

if __name__ == "__main__":
    exams, students, time_slots, rooms, room_slots = load_test("test2")

    G = build_conflict_graph(exams)
    coloring = welsh_powell_coloring(G)
    print(col_to_nodes(coloring))
    #c = print
    #def print(*args, **kwargsargs): 
    #    pass
    #schedule, penalty = assign_rooms_to_exams(coloring, exams, rooms, time_slots)
    # schedule = run_local_method(exams, time_slots, rooms)
    #print = c
    #print(check_exams_conflicts(schedule, exams))
    #print(check_room_capacities(schedule, rooms))
    run_tabu_method(exams, time_slots, rooms)