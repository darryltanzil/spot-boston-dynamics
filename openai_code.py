import os
from dotenv import load_dotenv
from openai import OpenAI
from enum import Enum
import base64
import json
import requests

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

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image? Keep your response around 2-3 sentences."
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

    return response.json()['choices'][0]['message']['content']



def main():
    input_text = "Hey Spot, turn around twice"
    #result = get_command_and_movement(input_text)
    img_response = identify_image("reference_img.jpg")
    # output = {
    #     "movement": result["degrees"],
    #     "command": Commands[result["command"]].value
    # }
    print(img_response)


if __name__ == "__main__":
    main()
