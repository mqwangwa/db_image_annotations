import PIL.Image
import os
import google.generativeai as genai
import dotenv
import typing_extensions as typing
import json

class Schema(typing.TypedDict):
    tree: bool
    crosswalk: bool
    stop_sign: bool
    traffic_light: bool
    chinese_calligraphy: bool
    bike_lane: bool
    fire_hydrant: bool
    sidewalk: bool


dotenv.load_dotenv(".env")
api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")

# schema = "{ tree: boolean, crosswalk: boolean, stop_sign: boolean, traffic_light: boolean, calligraphy: boolean }"

prompt = f"What do you see?"

node_id = "61283269"
angles = ["0", "90", "180", "270"]
pictures = [PIL.Image.open("data/"+node_id+"_"+angle+".jpg") for angle in angles]


genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(pictures+[prompt],
                                  generation_config=genai.GenerationConfig(
                                      response_mime_type="application/json", response_schema=list[Schema]
                                  ))
print(response.text)
print()

out = json.loads(response.text)
print(out)
