import json

# Charger les événements depuis le fichier JSON
with open("events.json", "r") as f:
    events = json.load(f)

# Filtrer les événements pour supprimer ceux de type "move"
filtered_events = [event for event in events if event["type"] != "move"]

# Sauvegarder les événements filtrés dans le fichier JSON
with open("events.json", "w") as f:
    json.dump(filtered_events, f, indent=4)

print("Les événements de type 'move' ont été supprimés.")