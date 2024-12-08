import pandas as pd
import pickle
import json

nodes_file = "osm/boston_chinatown_nodes.csv"
calligraphy_file = "boston_chinatown_results_gemini.pkl"
out_json_file = "boston_chinatown.json"

out = {}
with open(calligraphy_file, "rb") as f:
    calligraphy_results = pickle.load(f)
    df = pd.read_csv(nodes_file)

    for k in calligraphy_results:
        if calligraphy_results[k]["has_chinese_calligraphy"]:
            temp = {}
            temp_df = df.loc[df["osmid"] == int(k), :].iloc[0]
            temp["lat"] = temp_df["latitude"]
            temp["long"] = temp_df["longitude"]
            temp["words"] = calligraphy_results[k]["chinese_words"]
            out[k] = temp

with open(out_json_file, "w") as jf:
    json.dump(out, jf)