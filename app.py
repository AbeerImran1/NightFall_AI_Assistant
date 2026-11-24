import pyttsx3 # Text-to-speech library
# This library is used to convert text to speech, allowing the assistant to speak responses.
import speech_recognition as sr # Speech recognition library
import datetime # For getting the current date and time
import os # For interacting with the operating system
import webbrowser #For opening web pages in a browser
import logging # For logging errors
import random # for playing random music 
import requests # For weather 
import time # For adding delays

#Initalize the text-to-speech engine
engine  = pyttsx3.init()
user_name = "Mohammed"  # Name of the user 

# Set up logging 
logging.basicConfig(filename= "jarvis_errors.log", level=logging.ERROR,
                    format="%(asctime)s:%(levelname)s:%(message)s")

def speak(text):
    """Speak the given text using the text-to-speech engine."""
    engine.say(text)
    engine.runAndWait()
    
def listen():
    """Listen to the user's voice and return the recognized text."""
    recognizer = sr.Recognizer() # Create a recognizer object
    with sr.Microphone() as source: # Use the microphone as the audio source
        print("Listening...")
        audio = recognizer.listen(source) # Listens for audio input from the user

        try: 
            query = recognizer.recognize_google(audio) # Recognizes speech using Google Web Speech API
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            # If the speech is unintelligible
            speak("Repeat that again.")
            return ""
        except sr.RequestError:
            # If the API is unreachable
            speak("Sorry, the service is not available")
            return ""

def tell_time():
    """Tell the current time"""
    now = datetime.datetime.now() # Gets the current date and time 
    current_time = now.strftime("%I: %M %p") # Formats the time in 12-hour format with AM/PM
    speak(f"{user_name}, the time is {current_time}")

def search_google(query):
    speak(f"{user_name} I'm now searching for {query}")
    url = f"https://www.google.com/search?q={query}" # Create the search URL
    webbrowser.open(url) # Opens the URL in the default web broswer

def open_notepad():
    speak(f"I'm now opening notepad {user_name}")
    os.system("notepad.exe") # Runs Notepad

def change_user_name(new_name):
    global user_name
    user_name = new_name
    speak(f"Okay, I will call you {user_name} from now on.")

def play_music(music_dir="C:\\Users\\Abeer\\Music"):
    try:
        songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        if songs:
            song = random.choice(songs) # Randomly plays a song from the music directory
            speak(f"Playing {song}")
            os.startfile(os.path.join(music_dir, song)) # Opens the song file
        else: 
            speak("No music files found in the directory.")
    except Exception as e:
        logging.error(f"Error playing music: {e}")
        speak("Sorry, I couldn't play music.")


def get_weather(city):
    api_key = "9e4e1893812a072b752266829978c45c" # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get ("cod") == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            speak(f"The weather in {city} is currently {weather} with a temperature of {temp} degrees Celsius.")
        else:
            speak(f"Sorry, I couldn't find the weather information for {city}.")
    except Exception as e:
        logging.error(f"Error fetching weather: {e}")
        speak("Sorry, I couldn't get the weather information.")
    

def handle_command(command):
    try:
        command_map = {
            "exit": lambda: (speak(f"See you around! {user_name}"), exit()),
            "quit": lambda: (speak(f"See you around! {user_name}"), exit()),
            "hello": lambda: speak(f"Heyyy, how are you? {user_name} I am Jarvis"),
            "time": tell_time,
            "notepad": open_notepad,
            "play music": play_music, 
        }
        # Check mapped commands first
        for key, func in command_map.items():
            if key in command: 
                func()
                return 

        # Special cases (now outside the for loop)
        if "search for" in command:
            search_term = command.replace("search for", "").strip()
            if search_term: 
                search_google(search_term)
            else:
                speak(f"What is it you want me to help you search for? {user_name}")
                search_term = listen().lower()
                if search_term:
                    search_google(search_term)
            return
        elif "change my name to" in command:
            new_name = command.replace("change my name to", "").strip()
            if new_name:
                change_user_name(new_name)
            else:
                speak("What should I call you?")
                new_name = listen().strip()
                if new_name:
                    change_user_name(new_name)
            return
        elif "weather" in command:
            speak("For which city?")
            city = listen().strip()
            if city:
                get_weather(city)
            else:
                get_weather()
            return
        else: 
            error_msg = f"Unrecognized command: {command}"
            logging.error(error_msg)
            speak(f"Sorry, {user_name} I don't get it...")
            time.sleep(1)
            return
    except Exception as e:
        logging.error(f"Exception in handle_command: {e}")
        print(f"DEBUG ERROR: {e}")
        speak("I don't understand that command.")
        time.sleep(1)
        return


if __name__ == "__main__":
    # Main program starts here
    speak(f"Hello {user_name}, how can I help you?")
    wake_word = "jarvis" # The assistant will only respond if this word is in the command
    while True:
        command = listen().lower().strip() # Listen for a command and convert it to lowercase
        if not command:
            continue
        print(f"'{command}'") 
        if wake_word in command:
            # Remove the wake word from the command for easier processing
            command = command.replace(wake_word, "").strip()
            handle_command(command)
        else:
            # If the wake word was not detected
            print("Wake word not detected.")
        time.sleep(1) # Add a pause between the loops