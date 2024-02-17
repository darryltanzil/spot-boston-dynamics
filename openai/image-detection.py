import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
import json
import requests
import re

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

"""
Identifies the object in an image using the OpenAI API's image recognition model.

Parameters:
- image_path (str): The file path of the image to be analyzed.

Returns:
- dict: A dictionary containing the identified object and its characteristics.
"""
def identify_image(image_path):
    api_key = os.environ.get("OPENAI_API_KEY")

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    text = """
    What does the text on the main object say?
    Keep it 2 to 3 sentences, and return it as a JSON object in the form {"message":message_response}
    If you're not absolutely confident about everything that it says,
    suggest where to move the camera to position the object to the centre of the screen.
    If you are confident, don't mention anything related to the camera in your response.
    If repositioning is needed, produce a JSON object array in the format 
    {"command": command, "radians": radians_number} where the command value is one of the following commands:
    ['MOVE_LEFT', 'MOVE_RIGHT', 'MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP',
    'TURN_DOWN'] and whose radian value is, at most, set to 1. 
    If the main object is too big to be read, move backward. 
    If the main object is too small to be read, move forward. 
    If the main object is out of frame, either move left, move right, or turn the camera angle depending on what the most suitable option is. 
    If the camera angle needs to be adjusted, issue a turn command.
    Only respond with the JSON object, and nothing else. Do not include
    ```json ```.
    """
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # returns as a python dictionary
    return response.json()['choices'][0]['message']['content']

def main():
    img_response = identify_image("../QR3.jpg")
    json_response = json.loads(img_response)
    print(json_response)

if __name__ == "__main__":
    main()
