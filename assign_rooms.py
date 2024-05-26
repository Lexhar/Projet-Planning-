# Assigner aux différentes salles les examens en prenant les capacités et les nombres d'étudiants en compte
# A la sortie nous avons une solution initiale réalisable
def assign_rooms_to_exams(coloring, exams, rooms, time_slots):
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
