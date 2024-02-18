import speech_recognition as sr
import os


def listen_for_keyword(voice_callback):
    recognizer = sr.Recognizer()
    # microphone = sr.Microphone()

    # with microphone as source:
    #     print("Listening for 'hey spot'...")
    #     recognizer.adjust_for_ambient_noise(source)
    #     audio = recognizer.listen(source)
    
    print("Listening for 'hey spot'...")
    os.system("ffplay -autoexit audio/spot1.mp3")
    os.system(f"arecord -vv --format=cd --device={os.environ['AUDIO_INPUT_DEVICE']} -r 48000 --duration=5 -c 1 /tmp/temp.mp3")
    with sr.AudioFile("/tmp/temp.mp3") as source:
        audio = recognizer.record(source)

    try:
        os.system("ffplay -autoexit audio/spot2.mp3")
        print("Processing audio...")
        # Use Google Web Speech API for speech recognition
        command = recognizer.recognize_google(audio)
        if True:
        # if command.startswith("hey spot"):
            # Once the keyword is detected, continue listening for the command
            print("Keyword 'hey spot' detected.")
            voice_callback(command)
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
    listen_for_keyword(print)
