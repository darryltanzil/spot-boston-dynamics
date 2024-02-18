# import os
# import time
# import socket
# import subprocess
# import cv2
# import base64
# from wormholelite import CameraVideo
# from websocket import create_connection
# from ai_pipeline.input_delegator import delegate_input

# ROBOT_IP = "10.0.0.3"#os.environ['ROBOT_IP']
# SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
# SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']

# """
# 4 different states:

# Two methods to activate Spot:
# - Use Tensorflow 
# - Use Audio from Webcam (triggered by 'hey spot')

# Listening
# 1. use object detection API to walk towards object
# 2. take snapshot of project, send image to code processing Open AI
# 2.5 (if extra time) crop image before sending

# Processing
# 3. Once response is recieved, return back info in text
# Responding
# 4. Turn to person
# 5. Convert response into Text-to-speech, play through speaker
# 6. if possible, look at person and point to object 
# Idling
# """ 

# # def voice_callback(message):
#     # get

# def main():
#     if True:
#     # from spot_controller import SpotController
#     # with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
#         ws = create_connection("wss://737c-171-66-13-247.ngrok-free.app", ping_timeout=None)
#         ws.send("Hello, World")
#         # cam = CameraVideo(0, max_fps=1, height=360, width=480)
#         while True:
#             try:
#                 cmd =  ws.recv()
#                 if cmd == "[CAM]":
#                     frame = cam.get_frame()
#                     _, enc = cv2.imencode('.jpg', frame)
#                     jpg_as_text = base64.b64encode(enc)
#                     # print(jpg_as_text)
#                     ws.send(jpg_as_text)
#                     continue
#                 if cmd == "[PAYLOAD]":
#                     with open("/tmp/payload.py", "w+") as f:
#                         f.seek(0)
#                         f.truncate()
#                         f.write(ws.recv())
#                     try:
#                         process = subprocess.Popen(["python3", "/tmp/payload.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#                         for line in process.stdout:
#                             ws.send(line.strip())
#                         for line in process.stderr:
#                             ws.send(line.strip())
#                         process.wait()
#                     except Exception as e:
#                         ws.send(f"Error executing command: {e}")
#                     ws.send("[EOL]")
#                     continue
#                 res = eval(cmd)
#                 if res:
#                     ws.send(str(res))
#                 else:
#                     ws.send("None") 
#             except Exception as e:
#                 ws.send(str(e))


# if __name__ == '__main__':
#     main()

# import time
# time.sleep(50)
import speech_recognition as sr
import os


def read_out_loud(text_to_read):
    from gtts import gTTS
    print(text_to_read)  # Print the text to console for verification

    # Convert the extracted text to speech
    tts = gTTS(text=text_to_read, lang='en', slow=False)
    tts_file = "response_tts.mp3"
    tts.save(tts_file)

    # Play the generated speech file
    os.system(f"ffplay -autoexit {tts_file}")


# os.system("ffplay -autoexit audio/spot1.mp3")
# print("ok")
# import time
# time.sleep(4)

def listen_for_keyword(voice_callback):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for 'hey spot'...")
        os.system("ffplay -autoexit audio/spot1.mp3")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)

    try:
        print("Processing audio...")
        # Use Google Web Speech API for speech recognition
        command = recognizer.recognize_google(audio)
        if command.startswith("hey spot"):
            # Once the keyword is detected, continue listening for the command
            print("Keyword 'hey spot' detected.")
            os.system("ffplay -autoexit audio/spot2.mp3")
            voice_callback(command[len("hey spot "):])
        else:
            print("Keyword not detected. Listening again.")
            listen_for_keyword(voice_callback)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        listen_for_keyword(voice_callback)
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        listen_for_keyword(voice_callback)

if __name__ == "__main__":
    listen_for_keyword(read_out_loud)
