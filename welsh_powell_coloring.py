import networkx

# Algorithme de Welsh-Powell pour ressortir une coloration du graphe
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
