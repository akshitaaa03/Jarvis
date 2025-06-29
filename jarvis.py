from gpt4all import GPT4All             #IMPORTING MODULES
import pyttsx3
import speech_recognition as sr
import os
import random
import datetime
import pygame, pyaudio, pywhatkit, requests
#---------------------------------------------------------------
weather_API = "ceb94c73027a58062b3744375fb1c7a6"
Dfault_city = "Ahmedabad"
#-----------------------------------------------------------------------------------------------------
model_path = "C:\\Users\\DELL\\Desktop\\ak\\Jarvis\\Llama-3.2-3B-Instruct-Q4_0.gguf"
jarvis = GPT4All(model_path)
#--------------------------------------------------------------------------------------------------------
engine = pyttsx3.init()
recognizer = sr.Recognizer()
#--------------------------------------------------------------------------------------------------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={weather_API}&q={city}&units=metric"
    response = requests.get(url).json()
    if response["cod"] != "404":
        main = response["main"]
        weather = response["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        report = f"The weather in {city} is {weather} with {temp}°C and {humidity}% humidity."
        speak(report)
    else:
        speak("City not found.")
#-----------------------------------------------------------
def open_app(name): #THIS WILL LAUNCH APPS
     aname = name.lower()
     speak(f"opening {aname}!")
     if "chrome" in aname:
         os.system("start chrome")
     elif "notepad" in aname:
         os.system("start notepad")
     elif "calculator" in aname:
         os.system("start calc")
     elif "spotify" in aname:
         os.system("start spotify")
     else:
         print("APP IS NOT CONFIGURED!")

#-------------------------------------------------------------------------------
def play_music(): #PLAY MUSIC FROM SYSTEM FOLDER
    music_folder = "music"
    songs = [s for s in os.listdir(music_folder) if s.endswith(".mp3")]
    if not songs:
        speak("No songs found in your music folder.")
        return
    song = random.choice(songs)
    song_path = os.path.join(music_folder, song)
    speak(f"Playing {song}")
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
#-------------------------------------------------------------------------
def play_youtube(v_name): #PLAY VIDEOS ON YOUTUBE
    speak(f"Playing {v_name} on YouTube.")
    pywhatkit.playonyt(v_name)
#----------------------------------------------------------------------------

def speak(text):
    print("Jarvis:",text)
    engine.say(text)
    engine.runAndWait()
#-----------------------------------------------------------------------------
def listen():
    with  sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("SPEECH RECOGNITION ERROR!!!!")
#--------------------------------------------------------------------------
def tell_date_time():
    now = datetime.datetime.now()
    date = now.strftime("%A, %d %B %Y")  # Example: Monday, 28 June 2025
    time = now.strftime("%I:%M %p")      # Example: 06:45 PM
    speak(f"Today is {date} and the time is {time}.")


#---------------------------------------------------------
with jarvis.chat_session():
    print("Say 'HELLO JARVIS' to activate")
    intro = listen().lower()

    if "hello jarvis" in intro:
        speak("Hey Akshita, how may I assist you?")

        while True:
            command = listen()
            if not command:
                continue

            command = command.lower()

            if "bye" in command:
                speak("See you again, Akshita!")
                break
            elif "time" in command or "date" in command:
                tell_date_time()

            elif "play music" in command:
                play_music()

            elif "play" in command and "music" not in command:
                video = command.replace("play", "").strip()
                play_youtube(video)

            elif "open" in command or "launch" in command:
                app = command.replace("open", "").replace("launch", "").strip()
                open_app(app)

            elif "weather" in command:
                speak("Which city?")
                city = listen()
                if city:
                    get_weather(city)
                else:
                    get_weather(Dfault_city)

            else:
                reply = jarvis.generate(command)
                speak(reply)


#------------------------------------------------------------------------------------------                
                
        
    
 

    

