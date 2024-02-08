# Play audiosample
import os
audio_filename = "file_example_MP3_2MG.mp3"
os.system(f"ffplay -nodisp -t 6 -autoexit -loglevel quiet {audio_filename}")

# Capture image
import cv2
camera_capture = cv2.VideoCapture(0)
rv, image = camera_capture.read()
print(f"Image Dimensions: {image.shape}")
camera_capture.release()

# Capture audio sample
print("Start recording audio")
sample_name = "aaaa.wav"
os.system(f'arecord --device="hw:1,0" -vv --format=cd --duration=10 {sample_name}')
os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
