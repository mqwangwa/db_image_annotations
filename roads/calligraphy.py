# This file will be a specialized image annotation for identifying calligraphy.

import PIL.Image
import os
import google.generativeai as genai
from google.generativeai.types import generation_types
import dotenv
import typing_extensions as typing
import json
import pandas as pd
import time
import pickle
from tqdm import tqdm

dotenv.load_dotenv(".env")
api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
genai.configure(api_key=api_key)
prompt = f"Do you see Chinese calligraphy in the images? If so, what Chinese words do you see?"

class Schema(typing.TypedDict):
    has_chinese_calligraphy: bool
    chinese_words: list[str]

def force_required_fields(generation_config) -> dict:
    """
    Returns a copy with all fields in the schema marked as required.
    Workaround for https://github.com/google-gemini/generative-ai-python/issues/560.
    """
    generation_config = generation_types.to_generation_config_dict(generation_config)
    schema = generation_config["response_schema"]
    schema.required = list(schema.properties)
    return generation_config

generation_config = genai.GenerationConfig(
    response_mime_type="application/json",
    response_schema=Schema)
forced_generation_config = force_required_fields(generation_config)


total = {}
all_nodes = pd.read_csv("osm/oakland_chinatown_nodes.csv")
for node_id in tqdm(all_nodes["osmid"]):
    node_id = str(node_id)

    angles = ["0", "90", "180", "270"]
    pictures = [PIL.Image.open("data/"+node_id+"_"+angle+".jpg") for angle in angles]
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(pictures+[prompt],
                                        generation_config=forced_generation_config)
    except Exception as e:
        print(e)
        with open("oakland_chinatown_results_gemini.pkl", "wb") as f:
            pickle.dump(total, f)
        raise e
    
    output = json.loads(response.text) # Dict
    total[node_id] = output

    time.sleep(4.5) # Gemini free tier API limits you to 15 requests a minute 

with open("oakland_chinatown_results_gemini.pkl", "wb") as wf:
    pickle.dump(total, wf)