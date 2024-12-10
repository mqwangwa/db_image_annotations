# This file generates the annotated results

import google.generativeai as genai
import json
import pandas as pd
import time
from PIL import Image
import requests
from io import BytesIO
from schema_met_02 import Schema

SAMPLE_FRAC = 0.01
INPUT_FILE = "met_collection/datasets/FilteredObjects.xlsx"
OUTPUT_FILE = "met_collection/datasets/GeminiResults.xlsx"


def get_image_url(objectID):
    response = requests.get(
        f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}")
    output = json.loads(response.text)
    return output['primaryImage']


def make_requests():
    api_key = "AIzaSyAuzJFs7pUs25QzlxT1mlTuP9ljcNQtFJ0"
    genai.configure(api_key=api_key)
    prompt = f"What do you see?"
    objects = pd.read_excel(INPUT_FILE)
    objects = objects.sample(frac=SAMPLE_FRAC)
    count = 0
    results = []
    for objectID in objects["Object ID"]:
        try:
            # make a request to the Met API to get the URL of the image
            url = get_image_url(objectID)
            encoded_image = requests.get(url)
            # encode the image
            img = Image.open(BytesIO(encoded_image.content))
            # prompt Gemini for the data annotations
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([img]+[prompt],
                                              generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[Schema]
            ))
        except Exception as e:
            print(e)
            # output results early if an exception is raised
            pd.DataFrame(results).to_excel(OUTPUT_FILE, index=False)
            raise e

        outputs = (json.loads(response.text))[0]  # List[Dict]
        outputs["Object ID"] = objectID
        results.append(outputs)
        count += 1
        time.sleep(5)  # wait to account for rate limits
        if count % 50 == 0:
            print(f"{count} images processed")
    pd.DataFrame(results).to_excel(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    make_requests()
