import speech_recognition as sr

def main():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening... Say something:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Sorry, there was an error with the request: {str(e)}")

if __name__ == "__main__":
    main()
