"""
Creates a .csv file of each edge with their start node, end node, name, and length.
Creates a .csv file of each node and their (lat, long) coordinates.
"""

import osmnx as ox

def create_osm_csvs(osm_filepath, edges_output_path, nodes_output_path) -> None:
    """
    osm_filepath: name of the .osm file to look at (include .osm)
    edges_output_path: name of the edges output .csv file (include .csv)
    nodes_output_path : name of the nodes output .csv file (include .csv)
    """

    graph = ox.graph_from_xml(osm_filepath)
    nodes, edges = ox.graph_to_gdfs(graph)
    new_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"])

    unique_nodes = set()
    for idx, _ in new_edges.iterrows():
        u, v, _ = idx
        unique_nodes.add(u)
        unique_nodes.add(v)

    # edges
    new_edges.reset_index().loc[:, ["u", "v", "name", "length"]].rename(columns={"u": "start_node", "v": "end_node"}).to_csv(edges_output_path, index=False)

    # nodes
    formatted_nodes = nodes.reset_index()
    formatted_nodes.loc[formatted_nodes["osmid"].isin(unique_nodes), ["osmid", "y", "x"]].rename(columns={"y": "latitude", "x": "longitude"}).to_csv(nodes_output_path, index=False)


if __name__ == "__main__":
    create_osm_csvs("roads/cambridge.osm", "roads/cambridge_edges.csv", "roads/cambridge_nodes.csv")