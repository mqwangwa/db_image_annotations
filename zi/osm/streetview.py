# This file takes in the .osm nodes and gets the Google Street View images of them.

import os
import requests
import dotenv
import osmnx as ox
from tqdm import tqdm

dotenv.load_dotenv(".env")
api_key = os.environ.get("GOOGLE_STREET_VIEW_API_KEY")

osm_file = "osm/oakland_chinatown.osm"

graph = ox.graph_from_xml(osm_file)
nodes, edges = ox.graph_to_gdfs(graph)
valid_ways = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"]) # this should get all roads that a car can go on

unique_nodes = set()
for idx, _ in valid_ways.iterrows():
    u, v, _ = idx
    unique_nodes.add(u)
    unique_nodes.add(v)

for node in tqdm(unique_nodes):
    temp_df = nodes.loc[node, :]
    lat = temp_df["y"]
    long = temp_df["x"]

    # Define parameters
    location = f"{lat},{long}"
    size = "640x640"
    for heading in ["0", "90", "180", "270"]:
        street_view_url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={location}&heading={heading}&key={api_key}"

        # retry system
        for i in range(3):
            try:
                response = requests.get(street_view_url)
                if response.status_code == 200:
                    with open(f"data/{node}_{heading}.jpg", "wb") as file:
                        file.write(response.content)
                else:
                    continue

                break
            except Exception as e:
                print(e)
        else:
            print(f"the node {node} failed all retries")
