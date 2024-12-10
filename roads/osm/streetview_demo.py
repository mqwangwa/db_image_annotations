import os
import requests
import dotenv
import json

dotenv.load_dotenv(".env")
api_key = os.environ.get("GOOGLE_STREET_VIEW_API_KEY")

# Define parameters
location = "42.360159,-71.094885"  # Coordinates for San Francisco
size = "640x640"  # Image size
heading = "270"  # Camera direction


# Construct the URL
street_view_url = f"https://maps.googleapis.com/maps/api/streetview?size={size}&location={location}&heading={heading}&key={api_key}&return_error_code=true"

# Send a request to the API
response = requests.get(street_view_url)

# Check if the request was successful
if response.status_code == 200:
    # Save the image
    with open("testdata/street_view_image_4.jpg", "wb") as file:
        file.write(response.content)
    print("Street View image saved as 'street_view_image.jpg'.")
else:
    print(f"Error fetching image: {response.status_code}")
