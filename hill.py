import random
import folium
from map_creating import regions, edges

def build_graph(_regions, _edges):
    graph = {region: [] for region in _regions}
    for edge in _edges:
        a, b = edge
        graph[a].append(b)
    return graph


def has_conflict(graph, colors, node, color):
    for neighbor in graph[node]:
        if colors[neighbor] == color:
            return True
    return False


def count_conflicts(graph, colors):
    conflict_count = 0
    for node in graph:
        for neighbor in graph[node]:
            if colors[node] == colors[neighbor]:
                conflict_count += 1
    return conflict_count // 2 # dividing 2 because conflicts duplicates


def select_node_mrv(graph, colors, num_colors):
    mrv_node = None
    min_remaining_colors = num_colors + 1

    for node in graph:
        if any(colors[node] == colors[neighbor] for neighbor in graph[node]):
            remaining_colors = sum(1 for color in range(num_colors) if not has_conflict(graph, colors, node, color))
            if remaining_colors < min_remaining_colors:
                min_remaining_colors = remaining_colors
                mrv_node = node

    return mrv_node


def hill_climbing(graph, num_colors, max_side_steps=100):
    colors = {node: random.randint(0, num_colors - 1) for node in graph}
    current_conflicts = count_conflicts(graph, colors)

    side_steps = 0
    while side_steps < max_side_steps and current_conflicts > 0:
        node = select_node_mrv(graph, colors, num_colors)
        if node is None:
            break  #if no more conflicts

        for color in range(num_colors):
            if not has_conflict(graph, colors, node, color):
                previous_color = colors[node]
                colors[node] = color
                new_conflicts = count_conflicts(graph, colors)

                if new_conflicts < current_conflicts:
                    current_conflicts = new_conflicts
                    side_steps = 0
                else:
                    colors[node] = previous_color
        side_steps += 1

    return colors if current_conflicts == 0 else None


def random_restart_hill_climbing(graph, num_colors, max_side_steps=100, max_restarts=10000):
    for i in range(max_restarts):
        result = hill_climbing(graph, num_colors, max_side_steps)
        if result is not None:
            return result
    return None


my_graph = build_graph(regions, edges)
# my_colors = {0:'Red', 1:'Green', 2:'Blue', 3:'Black', 4:'Purple'}
# my_num_colors = 5
# my_colors = {0:'Red', 1:'Green', 2:'Blue', 3:'Black'}
# my_num_colors = 4
# my_colors = {0:'Red', 1:'Green', 2:'Blue'}
# my_num_colors = 3
my_colors = {0:'Red', 1:'Green', 2:'Blue',  3:'Black', 4:'Purple', 5:'Brown'}
my_num_colors = 6
solution = random_restart_hill_climbing(my_graph, my_num_colors)

if solution:
    hill_map = folium.Map(location=[48.3794, 31.1656], zoom_start=6)

    for edge in edges:
        region1, region2 = edge
        coord1 = [regions[region1]['lat'], regions[region1]['lon']]
        coord2 = [regions[region2]['lat'], regions[region2]['lon']]
        folium.PolyLine(locations=[coord1, coord2], color='gray', weight=2).add_to(hill_map)

    for node in regions:
        folium.CircleMarker(
            location=[regions[node]['lat'], regions[node]['lon']],
            radius=10,
            popup=f"{node} ({'black'})",
            color=my_colors[solution[node]],
            fill=True,
            fill_color=my_colors[solution[node]],
        ).add_to(hill_map)

    # saving map
    hill_map.save('hill_map.html')
else:
    print("NO SOLUTION")
    exit(0)