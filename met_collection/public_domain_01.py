# collect the Object IDs of images that fulfill our criteria
# build a labeled dataset in FilteredObjects.xlsx to use for validation
import pandas as pd


def filter_top_k(df_original, df_filtered, column_name, k):
    top_values = set(df_original[column_name].value_counts().head(k).index)
    top_values_filter = df_filtered[column_name].isin(top_values)
    df_filtered = df_filtered[top_values_filter]
    return df_filtered


def get_public_domain(df_original):
    public_domain_mask = df_original["Is Public Domain"]
    df_public_domain = df_original[public_domain_mask]
    return df_public_domain


if __name__ == "__main__":
    df_original = pd.read_excel("met_collection/datasets/MetObjects.xlsx")
    print("dataset loaded")
    df_public_domain = get_public_domain(df_original)
    print("dataset filtered by public domain")
    df_filtered = df_public_domain
    for column in ["Period", "Classification", "Culture", "Medium"]:
        df_filtered = filter_top_k(df_public_domain, df_filtered, column, 20)
        print(f"{column} filter applied")
    cols_to_keep = ["Object Number", "Object ID",
                    "Period", "Classification", "Culture", "Medium"]
    df_filtered = df_filtered[cols_to_keep]
    df_filtered.to_excel(
        "met_collection/datasets/FilteredObjects.xlsx", index=False)
