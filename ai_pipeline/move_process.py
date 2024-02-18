import os
from dotenv import load_dotenv
from openai import OpenAI
from enum import Enum
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
    TURN_UP = "TURN_UP"
    TURN_DOWN = "TURN_DOWN"

"""
Extracts command and movement information from a given text string using the OpenAI API.

Parameters:
- text (str): Input text containing the command and movement information.

Returns:
- dict: A dictionary with the extracted command and movement information.
"""

# CHANGE UNIT TO METRES FOR MOVING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# radians for turning is good though


def get_command_and_movement(text):
    enum_looped = [e.value for e in Commands]
    prompt = """
            Given the following string of text, produce a JSON object. The JSON object should be formatted as {"command": command, "radians"?: radians_number, "metres"?: metres: metres_number} where metres is chosen if we select a MOVE command 
    versus radians being chosen if we select a TURN command. You MUST include either radians (turning) or metres (moving). The command value should be
    one of the following commands: ['MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP', 'TURN_DOWN']. The metres or radians should be what the user specifies.
    However, if the user doesn't specify a number (e.g. they say "turn right a little bit"), use your judgement to determine a suitable amount for the output (e.g. a little is 0.5 radians, left turn is 2 radians, a lot is 4 radians, full circle is 8 radians)
            """

    print(prompt)

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

    # Now, 'content_dict' is a dictionary that you can work with
    command_array = content_dict["command"]

    # 'command_array' is now a list that contains the command and the movement

    print(content_dict)

    return content_dict

def main():
    input_text = "Hey Spot, look behind you"
    result = get_command_and_movement(input_text)
    output = {
        "movement": result["radians"],
        "command": Commands[result["command"]].value
    }

    print(output)

if __name__ == "__main__":
    main()
