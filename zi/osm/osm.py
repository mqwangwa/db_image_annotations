import osmnx as ox
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd

graph = ox.graph_from_xml("map.osm")
nodes, edges = ox.graph_to_gdfs(graph)
new_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"])

new_nodes = []
for idx, row in new_edges.iterrows():
    geom = row.geometry
    if geom.type == "LineString":
        # Extract start and end points
        start_point = Point(geom.coords[0])  # First coordinate
        end_point = Point(geom.coords[-1])  # Last coordinate
        new_nodes.append({"geometry": start_point, "type": "start"})
        new_nodes.append({"geometry": end_point, "type": "end"})

# Convert nodes to a GeoDataFrame
nodes_gdf = gpd.GeoDataFrame(new_nodes, crs=new_edges.crs)

print(nodes_gdf)
# Plot the nodes
nodes_gdf.plot(marker='o', color='blue', markersize=1)
plt.show()


# new_edges.plot(figsize=(10, 10), linewidth=1, color="gray")
# plt.show()

# l = []
# n = set()
# for idx, cols in new_edges.iterrows():
#     name = cols["name"]
#     ref = cols["ref"]
#     u, v, _ = idx
#     l.append((name, ref, u, v))
#     n.add(u)
#     n.add(v)

# print(l)
# print(len(n))

# print(nodes.loc[2501927209, :]) # 'y' is lat, 'x' is long
# print(nodes.loc[277667344, :]) 


# n = set()
# for idx, _ in nodes.iterrows():
#     n.add(idx)


