import speech_recognition as sr
import pyttsx3

# Define the wake words
WAKE_WORDS = ["nova", "hey nova", "are you there nova"]

def get_female_voice(engine):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice

def speak_text(text):
    engine = pyttsx3.init()
    get_female_voice(engine)
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def main():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening... Say something:")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        text = recognizer.recognize_google(audio).lower()

        # Check if any wake word is in the recognized text
        if any(wake_word in text for wake_word in WAKE_WORDS):
            response = "Yes, master. How can I help you?"
            print(f"Athena: {response}")
            speak_text(response)

            # Listen for a command (create a new source)
            with sr.Microphone() as command_source:
                print("Listening for a command...")
                recognizer.adjust_for_ambient_noise(command_source)
                command_audio = recognizer.listen(command_source, timeout=5, phrase_time_limit=5)
            
            command = recognizer.recognize_google(command_audio).lower()

            # Provide responses based on recognized commands
            if "good morning" in command or "morning" in command:
                response = "Good morning!"
            elif "who are you" in command or "about yourself" in command:
                response = "I'm just a computer program, but thanks for asking!"
            elif "thank you" in command:
                response = "You're welcome!"
            else:
                response = "I'm not sure how to respond to that."

            print(f"You said: {command}")
            print(f"Athena: {response}")
            speak_text(response)

    except sr.WaitTimeoutError:
        response = "Timeout: No speech detected."
        print(response)
        speak_text(response)
    except sr.UnknownValueError:
        response = "Sorry, I couldn't understand what you said."
        print(response)
        speak_text(response)
    except sr.RequestError as e:
        response = f"Sorry, there was an error with the request: {{str(e)}}"
        print(response)
        speak_text(response)

if __name__ == "__main__":
    main()
