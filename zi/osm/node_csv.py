# Creates a .csv file of each node and their (lat, long) coordinates.

import osmnx as ox

osm_file = "osm/oakland_chinatown.osm"
output_name = "oakland_chinatown_nodes.csv"

graph = ox.graph_from_xml(osm_file)
nodes, edges = ox.graph_to_gdfs(graph)
new_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"])

unique_nodes = set()
for idx, _ in new_edges.iterrows():
    u, v, _ = idx
    unique_nodes.add(u)
    unique_nodes.add(v)

# gets nodes
formatted_nodes = nodes.reset_index()
formatted_nodes.loc[formatted_nodes["osmid"].isin(unique_nodes), ["osmid", "y", "x"]].rename(columns={"y": "latitude", "x": "longitude"}).to_csv(output_name, index=False)