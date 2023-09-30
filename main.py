import speech_recognition as sr
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize

# Define wake words
WAKE_WORDS = ["kotha", "hi kotha", "hey kotha", "hello"]
EXIT_COMMANDS = ["close", "shutdown", "exit", "terminate"]

# Initialize NLTK
nltk.download("punkt")

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
                print("Listening...")  # Print "Listening..." message when actively listening
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

            text = recognizer.recognize_google(audio).lower()
            print(f"You: {text}")  # Print what you say to Kotha

            # Check if the wake word is recognized
            if any(wake_word in text for wake_word in WAKE_WORDS) and not program_active:
                program_active = True
                response = "Yes, I'm here. How can I assist you today?"
                speak_text(response)
                print("Kotha: " + response)
                continue  # Skip the rest of the loop for wake word

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
                response = "Have a good day, master!"
                print(response)
                speak_text(response)
                break  # Exit the program
            
            else:
                # Generate a response for not understanding
                not_understood_response = "I'm sorry, I didn't quite catch that. Can you please repeat?"
                print(f"Kotha: {not_understood_response}")
                speak_text(not_understood_response)

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
