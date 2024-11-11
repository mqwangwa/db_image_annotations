from utils import encode_image_to_base64, send_request_with_image, response_to_content

with open("schema.txt", "r") as f:
    schema = f.read()
    # image_id = "61283126_180"
    image_id = "61283218_90"
    request_text = f"""Given this schema {schema}, extract each field of the schema from the image
    and return the results in a JSON format. Return only the JSON. For the ID field, set it to {image_id}.
    Also add an estimate of how confident you are in your answers for each field extracted."""
    image_path = f"images/{image_id}.jpg"
    encoded_image = encode_image_to_base64(image_path)
    response = send_request_with_image(request_text, encoded_image)
    response_text = response_to_content(response)
    print(response_text)