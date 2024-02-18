import speech_recognition as sr


def listen_for_keyword(voice_callback):
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
        if command.startswith("hey spot"):
            # Once the keyword is detected, continue listening for the command
            print("Keyword 'hey spot' detected.")
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
    listen_for_keyword(print)
