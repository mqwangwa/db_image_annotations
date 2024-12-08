# Plots the edges that our map has.

import osmnx as ox
import matplotlib.pyplot as plt

osm_file = "osm/boston_chinatown.osm"

graph = ox.graph_from_xml(osm_file)
nodes, edges = ox.graph_to_gdfs(graph)
road_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"]) # should only get edges on a street road

road_edges.plot(figsize=(10, 10), linewidth=1, color="gray")
plt.show()