import os
from gtts import gTTS

# command is one of ['MOVE_FORWARD', 'MOVE_BACKWARD', 'TURN_LEFT', 'TURN_RIGHT', 'TURN_UP', 'TURN_DOWN']
def moveSpot(metres, command, spot):
    spot.move_head_in_points(yaws=[0], pitches=[0], rolls=[0])
    if command == "MOVE_FORWARD":
        spot.move_to_goal(goal_x=metres, goal_y=0)
    elif command == "MOVE_BACKWARD":
        spot.move_to_goal(goal_x=-metres, goal_y=0)
    print(metres)
    print(command)

def rotateSpot(radians, command, spot):
    if command == "TURN_LEFT":
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=1.0, cmd_duration=radians)
    elif command == "TURN_RIGHT":
        spot.move_by_velocity_control(v_x=0, v_y=0, v_rot=-1.0, cmd_duration=radians)
    elif command == "TURN_DOWN":
        spot.move_head_in_points(yaws=[0], pitches=[max(1.0, radians)], rolls=[0])
    elif command == "TURN_UP":
        spot.move_head_in_points(yaws=[0], pitches=[-max(1.0, radians)], rolls=[0])
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
