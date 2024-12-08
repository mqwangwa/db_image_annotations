# Counts the unique nodes for edges.

import osmnx as ox
import matplotlib.pyplot as plt

osm_file = "osm/oakland_chinatown.osm"

graph = ox.graph_from_xml(osm_file)
nodes, edges = ox.graph_to_gdfs(graph)
road_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"]) # should only get edges on a street road

l = []
n = set()
for idx, cols in road_edges.iterrows():
    name = cols["name"]
    ref = cols["ref"]
    u, v, _ = idx
    l.append((name, ref, u, v))
    n.add(u)
    n.add(v)

# print(l)
print(len(nodes))
print(len(n))