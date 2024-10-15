import folium
import random
from map_creating import regions, edges

iterations = 0
stucks = 0
avg_assignment_length = 0

def build_graph(_regions, _edges):
    graph = {region: [] for region in _regions}
    for edge in _edges:
        a, b = edge
        graph[a].append(b)
    return graph


def find_available_colors(node, graph, colors, assignment):
    available_colors = set(colors)
    for neighbor in graph[node]:
        if neighbor in assignment:
            available_colors.discard(assignment[neighbor])
            if not available_colors:
                break
    return available_colors


def select_unassigned_variable_mrv(graph, assignment, colors):
    unassigned = [v for v in graph if v not in assignment]
    min_remaining = float('inf')
    selected = None
    for vertex in unassigned:
        available = len(find_available_colors(vertex, graph, colors, assignment))
        if available < min_remaining:
            min_remaining = available
            selected = vertex
        if min_remaining == 0:
            break
    return selected


def backtrack(graph, colors, assignment):
    global iterations, stucks, avg_assignment_length
    if len(assignment) == len(graph):
        return assignment

    node = select_unassigned_variable_mrv(graph, assignment, colors)
    if node is None:
        return None # No solution

    for color in find_available_colors(node, graph, colors, assignment):
        assignment[node] = color
        avg_assignment_length += len(assignment)
        iterations += 1
        result = backtrack(graph, colors, assignment)
        if result:
            return result
        stucks += 1
        del assignment[node]
    return None


def graph_coloring(graph, colors):
    my_assignment = {}
    random_edge =  random.choice(list(regions.keys()))
    my_assignment[random_edge] = random.choice(colors)
    return backtrack(graph, colors, my_assignment)


my_graph = build_graph(regions, edges)
my_colors = ['Red', 'Green', 'Blue', 'Purple']

solution = graph_coloring(my_graph, my_colors)
if solution:
    backtracking_map = folium.Map(location=[48.3794, 31.1656], zoom_start=6)

    for edge in edges:
        region1, region2 = edge
        coord1 = [regions[region1]['lat'], regions[region1]['lon']]
        coord2 = [regions[region2]['lat'], regions[region2]['lon']]
        folium.PolyLine(locations=[coord1, coord2], color='gray', weight=2).add_to(backtracking_map)

    for node in regions:
        folium.CircleMarker(
            location=[regions[node]['lat'], regions[node]['lon']],
            radius=10,
            popup=f"{node} ({'black'})",
            color=solution[node],
            fill=True,
            fill_color=solution[node],
        ).add_to(backtracking_map)

    # saving map
    backtracking_map.save('backtracking_map.html')
else:
    print("NO SOLUTION")
    exit(0)

print(iterations, stucks, avg_assignment_length/iterations)