# Plots the nodes that make up the edges of our map.

import osmnx as ox
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd

osm_file = "osm/oakland_chinatown.osm"

graph = ox.graph_from_xml(osm_file)
nodes, edges = ox.graph_to_gdfs(graph)
road_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"]) # should only get edges on a street road

road_nodes = []
for idx, row in road_edges.iterrows():
    print(row)
    geom = row.geometry
    if geom.type == "LineString":
        # Extract start and end points
        start_point = Point(geom.coords[0])  # First coordinate
        end_point = Point(geom.coords[-1])  # Last coordinate
        road_nodes.append({"geometry": start_point, "type": "start"})
        road_nodes.append({"geometry": end_point, "type": "end"})

# Convert nodes to a GeoDataFrame
nodes_gdf = gpd.GeoDataFrame(road_nodes, crs=road_edges.crs)

# Plot the nodes
road_edges.plot(figsize=(10, 10), linewidth=1, color="gray")
nodes_gdf.plot(marker='o', color='blue', markersize=1)
nodes.plot(marker='o', color="blue", markersize=1)
plt.show()