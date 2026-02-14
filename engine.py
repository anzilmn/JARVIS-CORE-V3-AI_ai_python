import pyttsx3
import speech_recognition as sr
import os
from pygame import mixer

# Initialize Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 
engine.setProperty('rate', 190) 
engine.setProperty('volume', 1.0)

mixer.init()

# Global reference to the UI app to update the console
ui_app = None

def play_startup_sound():
    try:
        if os.path.exists("startup.mp3"):
            mixer.music.load("startup.mp3")
            mixer.music.play()
    except Exception as e:
        print(f"Startup sound skipped: {e}")

def speak(text):
    print(f"AYSHU: {text}")
    # Update UI if available
    if ui_app:
        ui_app.log_msg(f"AYSHU: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    r.energy_threshold = 300 
    r.pause_threshold = 0.6 
    
    with sr.Microphone() as source:
        if ui_app: ui_app.log_msg("SYSTEM: Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        if ui_app: ui_app.log_msg("SYSTEM: Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except Exception:
        return "none"