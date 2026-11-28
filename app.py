# app.py
import pyttsx3 
import speech_recognition as sr 
import datetime 
import os 
import webbrowser 
import logging 
import random 
import requests 
import time
import pyaudiowpatch as pyaudio
import sys
sys.modules['pyaudio'] = pyaudio
from dotenv import load_dotenv 

# Import the brain from your other file
from brain import ask_ai

# Load environment variables
load_dotenv()

engine = pyttsx3.init()
user_name = "Abeer" 

logging.basicConfig(filename="nightfall_errors.log", level=logging.ERROR,
                    format="%(asctime)s:%(levelname)s:%(message)s")

def speak(text):
    print(f"NightFall: {text}") 
    engine.say(text)
    engine.runAndWait()
    
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5) 
        audio = recognizer.listen(source)
        try: 
            query = recognizer.recognize_google(audio) 
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Sorry, the speech service is not available.")
            return ""

def tell_time():
    now = datetime.datetime.now() 
    current_time = now.strftime("%I:%M %p") 
    speak(f"{user_name}, the time is {current_time}")

def search_google(query):
    speak(f"{user_name}, I'm now searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}") 

def open_notepad():
    speak(f"I'm now opening notepad {user_name}")
    os.system("notepad.exe") 

def change_user_name(new_name):
    global user_name
    user_name = new_name
    speak(f"Okay, I will call you {user_name} from now on.")

def play_music(music_dir="C:\\Users\\Abeer\\Music"):
    try:
        songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        if songs:
            song = random.choice(songs) 
            speak(f"Playing {song}")
            os.startfile(os.path.join(music_dir, song)) 
        else: 
            speak("No music files found in the directory.")
    except Exception as e:
        logging.error(f"Error playing music: {e}")
        speak("Sorry, I couldn't play music.")

def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY", "YOUR_API_KEY_HERE")
    if api_key == "YOUR_API_KEY_HERE":
        speak("Please set up your weather API key first.")
        return
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            speak(f"The weather in {city} is currently {weather} with a temperature of {temp} degrees Celsius.")
        else:
            speak(f"Sorry, I couldn't find the weather information for {city}.")
    except Exception as e:
        logging.error(f"Error fetching weather: {e}")
        speak("Sorry, I couldn't get the weather information.")

def handle_command(command, chat_history):
    try:
        # --- Hardcoded Commands ---
        if "exit" in command or "quit" in command:
            speak(f"See you around! {user_name}")
            exit()
        elif "hello" in command or "hi" in command:
            speak(f"Heyyy, how are you? {user_name} I am NightFall.")
        elif "time" in command:
            tell_time()
        elif "notepad" in command:
            open_notepad()
        elif "play music" in command: 
            play_music()
        elif "search for" in command:
            search_term = command.replace("search for", "").strip()
            if search_term: 
                search_google(search_term)
            else:
                speak(f"What should I search for, {user_name}?")
                search_term = listen().lower()
                if search_term: search_google(search_term)
        elif "change my name to" in command:
            new_name = command.replace("change my name to", "").strip()
            if new_name:
                change_user_name(new_name)
            else:
                speak("What should I call you?")
                new_name = listen().strip()
                if new_name: change_user_name(new_name)
        elif "weather" in command:
            speak("For which city?")
            city = listen().strip()
            if city: get_weather(city)
        
        # --- AI Brain Fallback ---
        else: 
            # THIS IS WHERE THE STRAY CODE BELONGED
            ai_reply = ask_ai(command, chat_history)
            speak(ai_reply)
            
            # Update chat history so the AI remembers the conversation
            chat_history.append({"role": "user", "content": command})
            chat_history.append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        logging.error(f"Exception in handle_command: {e}")
        speak("I ran into an error trying to do that.")
        time.sleep(1)

if __name__ == "__main__":
    speak(f"Hello {user_name}, NightFall is online.")
    
    wake_word = "nightfall" 
    chat_history = [] 
    
    while True:
        command = listen().lower().strip() 
        if not command:
            continue
            
        if wake_word in command:
            command = command.replace(wake_word, "").strip()
            if not command:
                speak("Yes?")
                command = listen().lower().strip()

            if command:
                handle_command(command, chat_history)
        time.sleep(1) 