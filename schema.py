from utils import send_request_text_only, response_to_content

request_text = """ Given the following list of queries, propose a schema for a dataset of images of roads.
Each image will have a unique ID and we do not need to store the image data.
Format the response so that only the schema is provided and do so in a text-based format.
What is the proportion of protected to unprotected bike lanes?
Are there any obstructions in the bike lane (e.g. illegally parked cars, trash bins, etc.)?
Are these bike lanes biker-only or shared with pedestrians? Buses?
"""
response = send_request_text_only(request_text)
content = response_to_content(response)
with open('schema.txt', 'w') as f:
    if content:
        f.write(content)
    else:
        print("No content returned")
