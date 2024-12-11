"""
Transforms Gemini's CSV results into a JSON format.
Easier to run visualizations code.
"""

import pandas as pd
import json

def transform(nodes_csv_filepath, gemini_csv_filepath, output_json_filepath) -> None:
    nodes_df = pd.read_csv(nodes_csv_filepath)
    results_df = pd.read_csv(gemini_csv_filepath)
    out = {k:{} for k in results_df.columns if k != "node_id"} # {"column_name": {osmid: {"lat": int, "long": int}}}

    for _, row in results_df.iterrows():
        id = row["node_id"]
        temp_df = nodes_df.loc[nodes_df["osmid"] == int(id), :].iloc[0]
        coord = {"lat": temp_df["latitude"], "long": temp_df["longitude"]}

        for col in row.index:
            if col != "node_id":
                if row[col]:
                    out[col][str(id)] = coord

    with open(output_json_filepath, "w") as f:
        json.dump(out, f)

if __name__ == "__main__":
    transform("roads/cambridge_nodes.csv", "roads/cambridge_results_gemini.csv", "roads/cambridge_results.json")