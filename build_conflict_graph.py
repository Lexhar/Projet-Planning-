import networkx as nx

# Construire le graph de conflits entre les examens
# Si deux examens partagent la même arrête ils sont incompatibles
def build_conflict_graph(exams):
    G = nx.Graph()
    for exam in exams:
        G.add_node(exam['id'], students=exam['students'], duration=exam['duration'])
    for i, exam1 in enumerate(exams):
        for j, exam2 in enumerate(exams):
            if i < j and set(exam1['students']).intersection(exam2['students']):
                G.add_edge(exam1['id'], exam2['id'])
    return G
