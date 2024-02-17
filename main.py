import os
import time
import socket
from websocket import create_connection
from spot_controller import SpotController

ROBOT_IP = "10.0.0.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']

"""
4 different states:

Two methods to activate Spot:
- Use Tensorflow 
- Use Audio from Webcam (triggered by 'hey spot')

Listening
1. use object detection API to walk towards object
2. take snapshot of project, send image to code processing Open AI
2.5 (if extra time) crop image before sending

Processing
3. Once response is recieved, return back info in text
Responding
4. Turn to person
5. Convert response into Text-to-speech, play through speaker
6. if possible, look at person and point to object 
Idling
"""

def main():
    #example of using micro and speakers
    # print("Start recording audio")
    # sample_name = "aaaa.wav"
    # cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    # print(cmd)
    # os.system(cmd)
    # print("Playing sound")
    # os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
    
    # Capture image
    # import cv2
    # camera_capture = cv2.VideoCapture(0)
    # rv, image = camera_capture.read()
    # print(f"Image Dimensions: {image.shape}")
    # camera_capture.release()

    # Use wrapper in context manager to lease control, turn on E-Stop, power on the robot and stand up at start
    # and to return lease + sit down at the end
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
    # if True:
        # time.sleep(2)

        # # Move head to specified positions with intermediate time.sleep
        # spot.move_head_in_points(yaws=[0.2, 0],
        #                          pitches=[0.3, 0],
        #                          rolls=[0.4, 0],
        #                          sleep_after_point_reached=1)
        # time.sleep(3)

        # # Make Spot to move by goal_x meters forward and goal_y meters left
        # spot.move_to_goal(goal_x=0.5, goal_y=0)
        # time.sleep(3)

        # # Control Spot by velocity in m/s (or in rad/s for rotation)
        # spot.move_by_velocity_control(v_x=-0.3, v_y=0, v_rot=0, cmd_duration=2)
        # time.sleep(3)
        
        ws = create_connection("wss://6093-171-66-12-11.ngrok-free.app")
        ws.send("Hello, World")
        while True:
            try:
                cmd =  ws.recv()
                res = eval(cmd)
                if res:
                    ws.send(str(res))
                else:
                    ws.send("No response") 
            except Exception as e:
                ws.send(str(e))


if __name__ == '__main__':
    main()
