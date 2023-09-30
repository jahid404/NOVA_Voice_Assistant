import speech_recognition as sr
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize
import os
import openai

# Define wake words
WAKE_WORDS = ["kotha", "hi kotha", "hey kotha", "hello"]
EXIT_COMMANDS = ["close", "shutdown", "exit", "terminate"]

# Initialize NLTK
nltk.download("punkt")

# Initialize OpenAi
os.environ["OPEN_AI_API"] = "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"
openai.organization = "org-0cAwwpLXyuaKcOBiUk91p25c"
openai.api_key = os.getenv("OPEN_AI_API")

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
    conversation = []

    program_active = False
    response = "Hi master! How can I assist you today?"
    speak_text(response)
    print("Kotha: " + response)

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

            text = recognizer.recognize_google(audio).lower()
            print(f"You: {text}")

            # Check if the wake word is recognized
            if any(wake_word in text for wake_word in WAKE_WORDS) and not program_active:
                program_active = True
                response = "Yes, I'm here. How can I assist you today?"
                speak_text(response)
                print("Kotha: " + response)
                continue

            # If program_active is False, continue listening for wake word
            if not program_active:
                continue

            conversation.append(text)
            response = process_command(conversation)

            if response:
                print(f"Kotha: {response}")
                speak_text(response)
                conversation = []  # Clear conversation after Kotha's response

            # Check for exit commands
            elif any(exit_command in text for exit_command in EXIT_COMMANDS):
                response = "Have a good day master!"
                print(response)
                speak_text(response)
                break  # Exit the program
            
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": text + ' and reply with short description and natural as a human reply if possible.'
                        }
                    ]
                )
                print(f"Kotha: {response['choices'][0]['message']['content']}")
                speak_text(response['choices'][0]['message']['content'])

        except sr.WaitTimeoutError:
            pass  # Continue listening
        except sr.UnknownValueError:
            response = "I'm sorry, I didn't quite catch that. Can you please repeat?"
            print(response)
            speak_text(response)

def process_command(conversation):
    # Convert the conversation into a single string
    conversation_text = ' '.join(conversation)

    # Tokenize the text
    tokens = word_tokenize(conversation_text)

    if "good morning" in conversation_text or "morning" in conversation_text:
        return "Good morning!"
    elif "who are you" in conversation_text or "about yourself" in conversation_text:
        return "Thanks for your curiosity. My name is Kotha, and I'm here to assist you."
    elif "thank you" in conversation_text:
        return "You're welcome!"
    else:
        return None  # Return None for no response

if __name__ == "__main__":
    main()
