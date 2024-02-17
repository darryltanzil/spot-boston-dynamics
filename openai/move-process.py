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
    TURN_FORWARD = "TURN_FORWARD"
    TURN_BACKWARD = "TURN_BACKWARD"
    LOOK_LEFT = "TURN_LEFT"
    LOOK_RIGHT = "TURN_RIGHT"
    LOOK_FORWARD = "TURN_FORWARD"
    LOOK_BACKWARD = "TURN_BACKWARD"

"""
Extracts command and movement information from a given text string using the OpenAI API.

Parameters:
- text (str): Input text containing the command and movement information.

Returns:
- dict: A dictionary with the extracted command and movement information.
"""
def get_command_and_movement(text):
    enum_looped = [e.value for e in Commands]
    prompt = """
            Given the following string of text, produce a JSON object array in the format {"command":command, "degrees": degrees_number} where the command value is
    one of the following commands: ['MOVE_LEFT', 'MOVE_RIGHT', 'MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_FORWARD', 'TURN_BACKWARD']
    and whose degrees value represents a number from the range 0 to 360. 
    The JSON array's information should be gathered from the following text: Hey Spot, turn 90 degrees right.

    However, if the user doesn't specify a number (e.g. they say "turn right a little bit"), use your judgement to determine a suitable number for the output in the range.
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
    input_text = "Hey Spot, turn around twice"
    result = get_command_and_movement(input_text)
    output = {
        "movement": result["degrees"],
        "command": Commands[result["command"]].value
    }
    print(img_response)

if __name__ == "__main__":
    main()
