import pyautogui
import keyboard
import mouse
import time
import os
import json
from datetime import datetime

# Intervalle de temps entre chaque capture d'écran (en secondes)
TIME = 60

# Dossier pour sauvegarder les captures d'écran
screenshot_folder = "screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

# Liste pour stocker les événements
events = []

# Compteur de touches appuyées
key_press_count = 0

def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"{screenshot_folder}/screenshot_{timestamp}.png"
    pyautogui.screenshot(screenshot_path)
    events.append({
        "type": "screenshot",
        "timestamp": timestamp,
        "path": screenshot_path
    })
    print(f"Screenshot taken: {screenshot_path}")

def on_key_event(event):
    global key_press_count
    key_press_count += 1
    events.append({
        "type": "key",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "name": event.name,
        "event_type": event.event_type
    })
    print(f"Key event: {event.name} - {event.event_type}")

    # Prendre une capture d'écran toutes les 3 touches appuyées
    if key_press_count % 3 == 0:
        take_screenshot()

def on_click_event(event):
    if isinstance(event, mouse.ButtonEvent):
        events.append({
            "type": "click",
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "button": event.button,
            "event_type": event.event_type,
        })
        print(f"Click event: {event.button} - {event.event_type}")
    elif isinstance(event, mouse.MoveEvent):
        events.append({
            "type": "move",
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "position": (event.x, event.y)
        })
        print(f"Move event at {event.x}, {event.y}")

# Enregistrer les événements de clavier et de souris
keyboard.hook(on_key_event)
mouse.hook(on_click_event)

try:
    while True:
        time.sleep(TIME)
except KeyboardInterrupt:
    # Sauvegarder les événements dans un fichier JSON
    with open("events.json", "w") as f:
        json.dump(events, f, indent=4)
    print("Enregistrement terminé. Les événements ont été sauvegardés dans events.json.")