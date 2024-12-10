# This file generates the annotated results

import PIL.Image
import os
import google.generativeai as genai
import dotenv
import typing_extensions as typing
import json
import pandas as pd
import time
from schema_roads import Schema

dotenv.load_dotenv(".env")
api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
genai.configure(api_key=api_key)
prompt = f"What do you see?"

total = []
all_nodes = pd.read_csv("nodes.csv")
i = 0
for node_id in all_nodes["osmid"]:
    node_id = str(node_id)
    print(i)

    angles = ["0", "90", "180", "270"]
    pictures = [PIL.Image.open("data/"+node_id+"_"+angle+".jpg")
                for angle in angles]
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(pictures+[prompt],
                                          generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=list[Schema]
        ))
    except Exception as e:
        print(e)
        pd.DataFrame(total).to_csv("results.csv", index=False)
        raise e

    outputs = json.loads(response.text)  # List[Dict]
    temp = {k: False for k in Schema.__annotations__}
    for out in outputs:
        for k in temp:
            if k in out:  # if key isn't in the AI output, assume that the tag wasn't found in the pictures
                temp[k] = temp[k] or out[k]
    temp["node_id"] = node_id

    total.append(temp)
    i += 1
    time.sleep(5)  # Gemeni free tier API limits you to 15 requests a minute

pd.DataFrame(total).to_csv("gemini_labeled_roads.csv", index=False)
