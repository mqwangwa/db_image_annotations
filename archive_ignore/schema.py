from utils import send_request_text_only, response_to_content

request_text = """ Given the following list of queries, propose a schema for a dataset of images of roads.
Each image will have a unique ID and we do not need to store the image data.
Format the response so that only the schema is provided and do so in a text-based format.
Are these bike lanes protected by a barrier, protected by separation, or unprotected?
Are these bikes lanes obstruction-free, obstructed by cars, obstructed by trash bins, or obstructed by something else?
Are these bike lanes biker-only, shared with pedestrians, or shared with buses?
"""
response = send_request_text_only(request_text)
content = response_to_content(response)
with open('schema.txt', 'w') as f:
    if content:
        f.write(content)
    else:
        print("No content returned")
