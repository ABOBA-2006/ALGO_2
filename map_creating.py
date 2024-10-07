import networkx as nx
import folium


regions = {
    'Вінницька': {'lat': 49.2331, 'lon': 28.4682},
    'Волинська': {'lat': 50.7470, 'lon': 25.3310},
    'Дніпропетровська': {'lat': 48.4647, 'lon': 35.0462},
    'Донецька': {'lat': 48.0159, 'lon': 37.8028},
    'Житомирська': {'lat': 50.2547, 'lon': 28.6587},
    'Закарпатська': {'lat': 48.6208, 'lon': 22.2879},
    'Запорізька': {'lat': 47.8388, 'lon': 35.1396},
    'Івано-Франківська': {'lat': 48.9215, 'lon': 24.7097},
    'Київська': {'lat': 50.4501, 'lon': 30.5234},
    'Кіровоградська': {'lat': 48.5167, 'lon': 32.2667},
    'Луганська': {'lat': 48.5742, 'lon': 39.3078},
    'Львівська': {'lat': 49.8397, 'lon': 24.0297},
    'Миколаївська': {'lat': 46.9750, 'lon': 31.9946},
    'Одеська': {'lat': 46.4825, 'lon': 30.7233},
    'Полтавська': {'lat': 49.5883, 'lon': 34.5514},
    'Рівненська': {'lat': 50.6199, 'lon': 26.2516},
    'Сумська': {'lat': 50.9077, 'lon': 34.7983},
    'Тернопільська': {'lat': 49.5535, 'lon': 25.5948},
    'Харківська': {'lat': 49.9935, 'lon': 36.2304},
    'Херсонська': {'lat': 46.6354, 'lon': 32.6169},
    'Хмельницька': {'lat': 49.4204, 'lon': 26.9953},
    'Черкаська': {'lat': 49.4444, 'lon': 32.0594},
    'Чернігівська': {'lat': 51.4982, 'lon': 31.2893},
    'Чернівецька': {'lat': 48.2912, 'lon': 25.9393},
    'Крим': {'lat': 44.9521, 'lon': 34.1024},
}

edges = [
    ('Вінницька', 'Житомирська'),
    ('Вінницька', 'Черкаська'),
    ('Вінницька', 'Київська'),
    ('Вінницька', 'Одеська'),
    ('Вінницька', 'Чернівецька'),
    ('Вінницька', 'Кіровоградська'),
    ('Вінницька', 'Хмельницька'),

    ('Волинська', 'Рівненська'),
    ('Волинська', 'Львівська'),

    ('Дніпропетровська', 'Полтавська'),
    ('Дніпропетровська', 'Харківська'),
    ('Дніпропетровська', 'Запорізька'),
    ('Дніпропетровська', 'Донецька'),
    ('Дніпропетровська', 'Херсонська'),
    ('Дніпропетровська', 'Миколаївська'),
    ('Дніпропетровська', 'Кіровоградська'),

    ('Донецька', 'Луганська'),
    ('Донецька', 'Харківська'),
    ('Донецька', 'Запорізька'),
    ('Донецька', 'Дніпропетровська'),

    ('Житомирська', 'Вінницька'),
    ('Житомирська', 'Рівненська'),
    ('Житомирська', 'Київська'),
    ('Житомирська', 'Хмельницька'),

    ('Закарпатська', 'Івано-Франківська'),
    ('Закарпатська', 'Львівська'),

    ('Запорізька', 'Дніпропетровська'),
    ('Запорізька', 'Херсонська'),
    ('Запорізька', 'Донецька'),

    ('Івано-Франківська', 'Львівська'),
    ('Івано-Франківська', 'Тернопільська'),
    ('Івано-Франківська', 'Закарпатська'),
    ('Івано-Франківська', 'Чернівецька'),

    ('Київська', 'Вінницька'),
    ('Київська', 'Житомирська'),
    ('Київська', 'Черкаська'),
    ('Київська', 'Полтавська'),
    ('Київська', 'Чернігівська'),

    ('Кіровоградська', 'Черкаська'),
    ('Кіровоградська', 'Полтавська'),
    ('Кіровоградська', 'Дніпропетровська'),
    ('Кіровоградська', 'Миколаївська'),
    ('Кіровоградська', 'Одеська'),
    ('Кіровоградська', 'Вінницька'),

    ('Луганська', 'Донецька'),
    ('Луганська', 'Харківська'),

    ('Львівська', 'Волинська'),
    ('Львівська', 'Закарпатська'),
    ('Львівська', 'Івано-Франківська'),
    ('Львівська', 'Тернопільська'),
    ('Львівська', 'Рівненська'),

    ('Миколаївська', 'Одеська'),
    ('Миколаївська', 'Херсонська'),
    ('Миколаївська', 'Кіровоградська'),
    ('Миколаївська', 'Дніпропетровська'),

    ('Одеська', 'Миколаївська'),
    ('Одеська', 'Кіровоградська'),
    ('Одеська', 'Вінницька'),

    ('Полтавська', 'Дніпропетровська'),
    ('Полтавська', 'Кіровоградська'),
    ('Полтавська', 'Сумська'),
    ('Полтавська', 'Київська'),
    ('Полтавська', 'Черкаська'),
    ('Полтавська', 'Чернігівська'),
    ('Полтавська', 'Харківська'),

    ('Рівненська', 'Волинська'),
    ('Рівненська', 'Житомирська'),
    ('Рівненська', 'Хмельницька'),
    ('Рівненська', 'Тернопільська'),
    ('Рівненська', 'Львівська'),

    ('Сумська', 'Полтавська'),
    ('Сумська', 'Харківська'),
    ('Сумська', 'Чернігівська'),

    ('Тернопільська', 'Івано-Франківська'),
    ('Тернопільська', 'Чернівецька'),
    ('Тернопільська', 'Хмельницька'),
    ('Тернопільська', 'Рівненська'),
    ('Тернопільська', 'Львівська'),

    ('Харківська', 'Дніпропетровська'),
    ('Харківська', 'Донецька'),
    ('Харківська', 'Сумська'),
    ('Харківська', 'Полтавська'),
    ('Харківська', 'Луганська'),

    ('Хмельницька', 'Вінницька'),
    ('Хмельницька', 'Житомирська'),
    ('Хмельницька', 'Рівненська'),
    ('Хмельницька', 'Тернопільська'),
    ('Хмельницька', 'Чернівецька'),

    ('Черкаська', 'Кіровоградська'),
    ('Черкаська', 'Полтавська'),
    ('Черкаська', 'Київська'),
    ('Черкаська', 'Вінницька'),

    ('Чернігівська', 'Сумська'),
    ('Чернігівська', 'Київська'),
    ('Чернігівська', 'Полтавська'),

    ('Чернівецька', 'Івано-Франківська'),
    ('Чернівецька', 'Тернопільська'),
    ('Чернівецька', 'Хмельницька'),
    ('Чернівецька', 'Вінницька'),

    ('Крим', 'Херсонська'),

    ('Херсонська', 'Крим'),
    ('Херсонська', 'Миколаївська'),
    ('Херсонська', 'Дніпропетровська'),
    ('Херсонська', 'Запорізька'),
]

# creating Graph
G = nx.Graph()
G.add_nodes_from(regions.keys())
G.add_edges_from(edges)

# creating map
m = folium.Map(location=[48.3794, 31.1656], zoom_start=6)

for edge in G.edges():
    region1, region2 = edge
    coord1 = [regions[region1]['lat'], regions[region1]['lon']]
    coord2 = [regions[region2]['lat'], regions[region2]['lon']]
    folium.PolyLine(locations=[coord1, coord2], color='gray', weight=2).add_to(m)

for node in G.nodes():
    folium.CircleMarker(
        location=[regions[node]['lat'], regions[node]['lon']],
        radius=10,
        popup=f"{node} ({'black'})",
        color='black',
        fill=True,
        fill_color='black'
    ).add_to(m)

# saving map
m.save('ukraine_colored_graph_map.html')