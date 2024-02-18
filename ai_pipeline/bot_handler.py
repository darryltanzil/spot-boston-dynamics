import os
from gtts import gTTS

# command is one of ['MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP', 'TURN_DOWN']
def moveSpot(metres, command, spot):
    if command == "MOVE_FORWARD":
        spot.move_to_goal(goal_x=metres, goal_y=0)
    elif command == "MOVE_BACKWARD":
        spot.move_to_goal(goal_x=-metres, goal_y=0)
    print(metres)
    print(command)

def rotateSpot(radians, command, spot):
    if command == "TURN_LEFT":
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=0.5, cmd_duration=1.0)
    elif command == "TURN_RIGHT":
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=-0.5, cmd_duration=1.0)
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
