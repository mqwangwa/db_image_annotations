# Plots the nodes with calligraphy that make up the edges of our map.

import osmnx as ox
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd
import pickle
import pandas as pd

osm_file = "osm/boston_chinatown.osm"

graph = ox.graph_from_xml(osm_file)
nodes, edges = ox.graph_to_gdfs(graph)
road_edges = edges[edges.index.get_level_values("key") == 0].dropna(subset=["maxspeed"]) # should only get edges on a street road

# get the nodes that have calligraphy
with open("boston_chinatown_results_gemini.pkl", "rb") as f:
    results = pickle.load(f)

has_calligraphy_nodes = set()
for k in results:
    if "has_chinese_calligraphy" in results[k]:
        if results[k]["has_chinese_calligraphy"]:
            has_calligraphy_nodes.add(int(k))
    else:
        print(f"{k} doesn't have the 'has_chinese_calligraphy' attribute")


df = pd.read_csv("osm/boston_chinatown_nodes.csv")
filtered_df = df.loc[df["osmid"].isin(has_calligraphy_nodes), :]

df["geometry"] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
filtered_df["geometry"] = filtered_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

# original
orig_gdf = gdf = gpd.GeoDataFrame(df, geometry='geometry')
orig_gdf.set_crs(epsg=4326, inplace=True)
orig_gdf.plot(marker='o', color='blue', markersize=1)

# filtered
gdf = gpd.GeoDataFrame(filtered_df, geometry='geometry')
gdf.set_crs(epsg=4326, inplace=True)
gdf.plot(marker='o', color='blue', markersize=1)

plt.show()