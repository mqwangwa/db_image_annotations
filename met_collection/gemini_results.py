# This file generates the annotated results

import os
import google.generativeai as genai
import dotenv
import typing_extensions as typing
import json
import pandas as pd
import time
from PIL import Image
import requests
from io import BytesIO
import enum
from schema_met import Schema


def get_image_url(objectID):
    response = requests.get(
        f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}")
    output = json.loads(response.text)
    return output['primaryImage']


def make_requests():
    api_key = "AIzaSyAuzJFs7pUs25QzlxT1mlTuP9ljcNQtFJ0"
    genai.configure(api_key=api_key)
    prompt = f"Describe this artwork."
    objects = pd.read_excel("FilteredObjects.xlsx")
    objects = objects.sample(frac=0.01)
    count = 0
    results = []
    print(len(objects))
    for objectID in objects["Object ID"]:
        try:
            url = get_image_url(objectID)
            encoded_image = requests.get(url)
            img = Image.open(BytesIO(encoded_image.content))
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([img]+[prompt],
                                              generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[Schema]
            ))
        except Exception as e:
            print(e)
            pd.DataFrame(results).to_excel("results.xlsx", index=False)
            raise e

        outputs = (json.loads(response.text))[0]  # List[Dict]
        outputs["Object ID"] = objectID
        results.append(outputs)
        count += 1
        time.sleep(5)
        if count % 50 == 0:
            print(f"{count} images processed")
    pd.DataFrame(results).to_excel("results.xlsx", index=False)


if __name__ == "__main__":
    make_requests()
