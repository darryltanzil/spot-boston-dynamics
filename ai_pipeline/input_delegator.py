import os
from dotenv import load_dotenv
from openai import OpenAI
from enum import Enum
from ai_pipeline.bot_handler import moveSpot, rotateSpot, playAudio
from ai_pipeline.image_detection import process_image
from ai_pipeline.misc_request import get_openai_command
from ai_pipeline.move_process import get_command_and_movement
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

"""
Extracts command and movement information from a given text string using the OpenAI API.

Parameters:
- text (str): Input text containing the command and movement information.

Returns:
- dict: A dictionary with the extracted command and movement information.
"""
def delegate_input(text, spot):
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
        return process_image(spot)
    elif content_dict["type"] == "movement":
        command = get_command_and_movement(content_dict["prompt"])
        if "message" not in command:
            if "radians" in command:
                rotateSpot(command["radians"], command["command"], spot)
            elif "metres" in command:
                moveSpot(command["metres"], command["command"], spot)
    else:
        return get_openai_command(content_dict["prompt"])

# playAudio(delegate_input("Hey spot, move to the left a little"))
