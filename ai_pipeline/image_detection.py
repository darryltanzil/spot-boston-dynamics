import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
import json
import requests
import cv2
import re

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def process_image():
    """
    Call this method whenever you want to screenshot and process whatever the robot is looking at right now.
    """
    base64_image = snapshot_image()
    identified_image = identify_image(base64_image)
    if "message" not in identified_image:
        return process_image()
    else:
        return identified_image["message"]

def snapshot_image():
    """
    Takes a snapshot using the Open CV 2 library.
    """

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Read a frame from the camera
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Check if the frame was captured successfully
    if ret:
        # Encode the image as a JPEG
        _, buffer = cv2.imencode('.jpg', frame)

        cv2.imwrite("test", frame)

        # Encode the image as a JPEG
        # Convert the JPEG buffer to a base64 string
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Return the base64 string
        return jpg_as_text
    else:
        print("Error: Could not capture an image.")
        return None


"""
Identifies the object in an image using the OpenAI API's image recognition model.

Parameters:
- image_path (str): The file path of the image to be analyzed.

Returns:
- dict: A dictionary containing the identified object and its characteristics.
"""
def identify_image(base64_image):
    api_key = os.environ.get("OPENAI_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    text = """
    What does the poster on the window say?
    If you are confident that it is readable: Keep it to 2 or 3 sentences, and return it as a JSON object in the form {"message":message_response}. Don't mention anything related to the camera in your response.

    If you're not absolutely confident about everything that it says, suggest where to move the camera in order to position the poster 
    on the window to the centre of the screen. The end goal is that the poster should be readable. Do this according to the following rules:
    If repositioning is needed, select one of the following commands: ['MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP',
    'TURN_DOWN']. 
    The command should be formatted as {"command": command, "radians"?: radians_number, "metres"?: metres: metres_number} where metres is chosen if we select a MOVE command 
    versus radians being chosen if we select a TURN command. 
    If the poster on the window is too big to be read, MOVE_BACKWARD. 
    If the poster on the window is too small to be read, MOVE_FORWARD. 
    If the poster on the window is out of frame, either TURN_LEFT or TURN_RIGHT depending on what makes the poster more readable and more centered.
    Only respond with the JSON object, and nothing else. Do not include ```json```.
    """

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
    # If the poster on the window is out of frame, either TURN_LEFT or TURN_RIGHT depending on what makes the poster more readable.
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
    # img_response = identify_image("../test_images/shitty_poster3.jpg")
    img_response = process_image()
    json_response = json.loads(img_response)
    print(json_response)


if __name__ == "__main__":
    main()
