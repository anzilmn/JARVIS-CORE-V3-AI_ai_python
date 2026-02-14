import webbrowser
import os
import pywhatkit
import re
import engine # Important to use the updated engine
from AppOpener import open as open_app 

def search_and_open_shortcut(app_name):
    paths = [
        os.path.join(os.environ['PROGRAMDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
        os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
    ]
    for p in paths:
        if os.path.exists(p):
            for root, dirs, files in os.walk(p):
                for file in files:
                    if app_name.lower() in file.lower() and file.endswith(".lnk"):
                        os.startfile(os.path.join(root, file))
                        return True
    return False

def perform_action(query):
    query = query.lower().strip()

    if query.startswith('open'):
        target = query.replace("open", "").strip()
        if search_and_open_shortcut(target):
            engine.speak(f"Launching {target}, vro.")
            return
        try:
            open_app(target, match_closest=True)
            engine.speak(f"Accessing {target}")
            return
        except:
            if any(ext in target for ext in ['.com', '.in', '.org', '.net']):
                engine.speak(f"Navigating to {target}")
                webbrowser.open(f"https://{target}")
            else:
                engine.speak(f"Searching Google for {target}")
                webbrowser.open(f"https://www.google.com/search?q={target}")
            return

    if 'message' in query or 'send' in query:
        number_match = re.search(r'\d{10,12}', query)
        if number_match:
            phone_no = number_match.group()
            phone_no = phone_no if phone_no.startswith('+') else f"+91{phone_no}"
            msg = "Hello!" 
            for sep in ["saying", "message", "that", "to"]:
                if sep in query:
                    msg = query.split(sep)[-1].strip()
                    break
            engine.speak(f"Initializing WhatsApp transmission to {phone_no}")
            pywhatkit.sendwhatmsg_instantly(phone_no, msg, 15, True, 2)
        else:
            engine.speak("Vro, I need a phone number.")
        return

    if 'search' in query:
        term = query.replace("search", "").strip()
        engine.speak(f"Searching for {term}")
        webbrowser.open(f"https://www.google.com/search?q={term}")
    elif 'play' in query:
        song = query.replace("play", "").strip()
        engine.speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    elif any(word in query for word in ['exit', 'stop', 'shutdown']):
        engine.speak("Ayshu powering down. Stay safe, vro!")
        os._exit(0)
    else:
        engine.speak("Searching web for intel.")
        webbrowser.open(f"https://www.google.com/search?q={query}")