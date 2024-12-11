"""
Uses Google's Gemini to generate the annotated results.
"""

import PIL.Image
import os
import google.generativeai as genai
import dotenv
import typing_extensions as typing
import json
import pandas as pd
import time
from tqdm import tqdm

dotenv.load_dotenv(".env")
api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
genai.configure(api_key=api_key)

schema_translate = {
    "bool": bool
}

def annotate(schema_str, nodes_csv_filepath, output_csv_filepath) -> None:
    """
    schema_str: the schema passed in from the user in the main page (should be in JSON string form)
    nodes_csv_filepath: filepath of the nodes csv file for your map data
    output_filepath: where the resulting .csv file will be stored (should end in .csv)
    """

    prompt = f"What do you see?"

    # create Python schema representation
    class Schema(typing.TypedDict):
        pass

    input_schema = json.loads(schema_str)
    for k in input_schema:
        if input_schema[k] not in schema_translate:
            raise Exception("types other than 'bool' are currently not supported for the map visualization")

        Schema.__annotations__[k] = schema_translate[input_schema[k]]

    # run gemini
    total = []
    all_nodes = pd.read_csv(nodes_csv_filepath)
    for node_id in tqdm(all_nodes["osmid"]):
        node_id = str(node_id)

        angles = ["0", "90", "180", "270"]
        pictures = [PIL.Image.open("data/"+node_id+"_"+angle+".jpg") for angle in angles]
        try:
            model = genai.GenerativeModel("gemini-1.5-flash") ## REPLACE ME to use a different Gemini model
            response = model.generate_content(pictures+[prompt],
                                            generation_config=genai.GenerationConfig(
                                                response_mime_type="application/json", response_schema=list[Schema]
                                            ))
        except Exception as e:
            print(e)
            pd.DataFrame(total).to_csv(output_csv_filepath, index=False)
            raise e

        outputs = json.loads(response.text) # List[Dict]
        temp = {k:False for k in Schema.__annotations__}
        for out in outputs:
            for k in temp:
                if k in out: # if key isn't in the AI output, assume that the tag wasn't found in the pictures
                    temp[k] = temp[k] or out[k]
        temp["node_id"] = node_id

        total.append(temp)
        time.sleep(5) # Gemeni free tier API limits you to 15 requests a minute

    pd.DataFrame(total).to_csv(output_csv_filepath, index=False)