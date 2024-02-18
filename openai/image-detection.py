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

    thingToRead = "flyer"

    text = f"""
    [What does the {thingToRead} say?]
    If you are confident that it is readable: Keep it to 2 sentences, and return it as a JSON object in the form {{"message":message_response}}. Don't mention anything related to the camera in your response.

    If you're not absolutely confident about everything that it says, suggest where to move the camera in order to position the {thingToRead} to the centre of the screen. 
    The end goal is that the poster should be readable. Do this according to the following rules:
    If repositioning is needed, select one of the following commands: ['MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP',
    'TURN_DOWN']. 
    The command should be formatted as {{"command": command, "radians"?: radians_number, "metres"?: metres: metres_number}} where metres is chosen if we select a MOVE command 
    versus radians being chosen if we select a TURN command. 
    If the {thingToRead} is too big to be read, MOVE_BACKWARD. 
    If the {thingToRead} is too small to be read, MOVE_FORWARD. 
    If the {thingToRead} is not fully in the photo, either TURN_LEFT or TURN_RIGHT depending on what makes the poster more centered and easier to read.
    Only respond with the JSON object, and nothing else. Do not include ```json```.
    """

    # terms like 'out of frame' and 'readable' are too vague. be more specific overall
    # square brackets around main objective
    # prompt is too long & is too much like english 
    # llm doesn't necessarily know that words are on the poster 
    # ask GPT for advice on the prompt framing 
    # look up best practices for prompt engineering

    


    # Keep it 2 to 3 sentences, and return it as a JSON object in the form {"message":message_response}
    # If you're not absolutely confident about everything that it says,
    # suggest where to move the camera to position the poster on the window to the centre of the screen.
    # If you are confident, don't mention anything related to the camera in your response.
    # If repositioning is needed, produce a list of commands 
    # {"command": command, "radians"?: radians_number, "metres"?: metres: metres_number} where metres is chosen if we select a MOVE command 
    # versus radians being chosen if we select a TURN command. 
    # the command value is one of the following commands:
    # ['MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP',
    # 'TURN_DOWN'] the radian value or the metre value is, at most, set to 1. 
    # If the poster on the window is too big to be read, MOVE_BACKWARD. 
    # If the poster on the window is too small to be read, MOVE_FORWARD. 
    # If the poster on the window is out of frame, either TURN_LEFT, TURN_RIGHT, TURN_UP or TURN_DOWN depending on what makes the poster more readable.
    # If the poster starts off as unreadable, the end goal is that the poster should be readable.
    # Only respond with the JSON object, and nothing else. Do not include
    # ```json ```.
    
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
    img_response = identify_image("../test_images/QR3.jpg")
    json_response = json.loads(img_response)
    print(json_response)

if __name__ == "__main__":
    main()
