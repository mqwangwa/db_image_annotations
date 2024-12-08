import pandas as pd
import pickle

j = {
    "123": {
        "a": True,
        "b": False,
        "c": True,
    },
    "764": {
        "a": False,
        "b": False,
        "c": False,
    }
}

# with open("test.pkl", "wb") as f:
#     pickle.dump(j, f)
#
# with open("test.pkl", "rb") as rf:
#     d = pickle.load(rf)
#     print(d)


with open("oakland_chinatown_results_gemini.pkl", "rb") as f:
    d = pickle.load(f)
    total = 0
    for k in d:
        if d[k]["has_chinese_calligraphy"]:
            total += 1

    print(total)