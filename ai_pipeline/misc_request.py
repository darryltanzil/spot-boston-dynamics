import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

"""
    Sends a text message to the OpenAI API and returns the response.

    Parameters:
    - text (str): The input text string to be sent to the OpenAI API.

    Returns:
    - str: The response content from the OpenAI API.
"""
def get_openai_command(text):

    # Make a call to the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        max_tokens=100
    )
    content_string = response.choices[0].message.content

    return content_string

def main():
    input_text = "Can you tell me what 9 + 10 is?"
    result = get_openai_command(input_text)
    print(result)

if __name__ == "__main__":
    main()
