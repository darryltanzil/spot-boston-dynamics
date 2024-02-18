import speech_recognition as sr

def listen_for_keyword():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for 'hey spot'...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Processing audio...")
        # Use Google Web Speech API for speech recognition
        command = recognizer.recognize_google(audio)
        if "hey spot" in command.lower():
            # Once the keyword is detected, continue listening for the command
            print("Keyword 'hey spot' detected.")
            listen_for_command()
        else:
            print("Keyword not detected. Listening again.")
            listen_for_keyword()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        listen_for_keyword()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        listen_for_keyword()

def listen_for_command(voice_callback):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Processing command...")
        command = recognizer.recognize_google(audio)
        voice_callback(command)
    except sr.UnknownValueError:
        print("Sorry, I could not understand the command.")
        listen_for_command()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        listen_for_command()

if __name__ == "__main__":
    listen_for_keyword()
