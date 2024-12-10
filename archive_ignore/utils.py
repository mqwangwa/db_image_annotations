import requests
import json
import ast
import base64

# OPENROUTER_API_KEY = "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" # margaret
# OPENROUTER_API_KEY = "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" # zi
# OPENROUTER_API_KEY = "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"  # anne
# OPENROUTER_API_KEY = "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" # margaret #2
# OPENROUTER_API_KEY = "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"  # lucas
OPENROUTER_API_KEY = "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"  # katie


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return "data:image/jpeg;base64," + encoded_string


def send_request_with_image(request_text, image_encoding):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": "meta-llama/llama-3.2-90b-vision-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": request_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_encoding
                            }
                        }
                    ]
                }
            ]

        })
    )
    return response


def send_request_text_only(request_text):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": "meta-llama/llama-3.2-90b-vision-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": request_text
                        }
                    ]
                }
            ]

        })
    )
    return response


def response_to_content(response):
    try:
        response_contents = response.json()
        content = response_contents['choices'][0]['message']['content']
        if content[0] == "[":
            content_list = ast.literal_eval(content)
            return content_list[0]['text']
        else:
            return content
    except KeyError as e:
        print(response.content)
        print(f"KeyError found, probably rate limited {e}")
    except Exception as e:
        print(response.content)
        print(f"Other exception when trying to get response contents {e}")
