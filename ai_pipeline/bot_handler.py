import os
from gtts import gTTS

# command is one of ['MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP', 'TURN_DOWN']
def moveSpot(metres, command):
    spot = globals().get("spot_global", None)
    spot.move_to_goal(goal_x=0.3, goal_y=0)
    print(metres)
    print(command)

def rotateSpot(radians, command):
    spot = globals().get("spot_global", None)
    spot.move_to_goal(goal_x=-0.3, goal_y=0)
    print(radians)
    print(command)

def playAudio(text):
    print(f"{text=}")
    if text == None:
        return
    # Convert the extracted text to speech
    tts = gTTS(text=text, lang='en', slow=False)
    tts_file = "response_tts.mp3"
    tts.save(tts_file)

    # Play the generated speech file
    os.system(f"ffplay -autoexit {tts_file}")
