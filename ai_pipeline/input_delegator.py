import os
from dotenv import load_dotenv
from openai import OpenAI
from enum import Enum
from image_detection import process_image
from misc_request import get_openai_command
from move_process import get_command_and_movement
import json

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

class Commands(Enum):
    MOVE_LEFT = "MOVE_LEFT"
    MOVE_RIGHT = "MOVE_RIGHT"
    MOVE_FORWARD = "MOVE_FORWARD"
    MOVE_BACKWARD = "MOVE_BACKWARD"
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"
    TURN_FORWARD = "TURN_UP"
    TURN_BACKWARD = "TURN_DOWN"



# CHANGE UNIT TO METRES FOR MOVING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# radians for turning is good though



"""
Extracts command and movement information from a given text string using the OpenAI API.

Parameters:
- text (str): Input text containing the command and movement information.

Returns:
- dict: A dictionary with the extracted command and movement information.
"""
def delegate_input(text):
    enum_looped = [e.value for e in Commands]
    prompt = """
    Given the following string of text, determine whether it is focused on asking for an image,
    asking for movement, or asking for a general inquiry. Return the output as a JSON object in the following form: 
    {"type": (either "movement", "image_process", or "general"), "prompt":"prompt"}"""

    # Make a call to the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": text,
            }
        ],
    )

    print(response)

    # Assuming 'response' is the response from the OpenAI API
    content_string = response.choices[0].message.content

    # Remove leading and trailing whitespace
    content_string = content_string.strip()

    # Convert the string to a dictionary
    content_dict = json.loads(content_string)

    print(content_dict)
    if content_dict["type"] == "image_process":
        return process_image()
    elif content_dict["type"] == "movement":
        return get_command_and_movement(content_dict["prompt"])
    else:
        return get_openai_command(content_dict["prompt"])

print(delegate_input("Hey spot, what's 9 + 10"))