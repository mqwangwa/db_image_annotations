# Creates a .csv file of each edge with their start node, end node, name, and length.

import osmnx as ox

osm_file = "osm/oakland_chinatown.osm"
output_name = "osm/oakland_chinatown_roads.csv"

graph = ox.graph_from_xml(osm_file)
nodes, edges = ox.graph_to_gdfs(graph)
new_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"])

unique_nodes = set()
for idx, _ in new_edges.iterrows():
    u, v, _ = idx
    unique_nodes.add(u)
    unique_nodes.add(v)

new_edges.reset_index().loc[:, ["u", "v", "name", "length"]].rename(columns={"u": "start_node", "v": "end_node"}).to_csv(output_name, index=False)