import pandas as pd

df = pd.read_csv("osm/boston_chinatown_nodes.csv")

print(df.loc[df["osmid"] == 61341714, :].iloc[0]["latitude"])