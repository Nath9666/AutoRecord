import speech_recognition as sr
from pydub import AudioSegment
import os

# Charger le fichier audio
audio_path = "./record/BlenderFormation.wav"  # Remplacer par le chemin de votre fichier audio
text_path = audio_path.replace("record", "txt").replace(".wav", ".txt")
audio = AudioSegment.from_file(audio_path)

# Vérifier la durée du fichier audio
duration_seconds = audio.duration_seconds
segment_duration = 180 * 1000  # 3 minutes en millisecondes

# Créer les dossiers temp et txt
os.system("mkdir temp")
os.system("mkdir txt")

if duration_seconds > 180:  # 3 minutes = 180 secondes
    print("Le fichier audio dépasse 3 minutes. Découpage en segments de 3 minutes...")
    
    # Découper le fichier audio en segments de 3 minutes
    for i in range(0, len(audio), segment_duration):
        segment = audio[i:i + segment_duration]
        segment_path = f"./temp/segment_{i // segment_duration + 1}.wav"
        segment.export(segment_path, format="wav")
        print(f"Segment {i // segment_duration + 1} enregistré : {segment_path}")
else:
    print("Le fichier audio est valide et ne dépasse pas 3 minutes.")

# Créer un objet Recognizer
recognizer = sr.Recognizer()

files = os.listdir("./temp")

for file in files:
    # Ouvrir le fichier audio
    with sr.AudioFile(f"./temp/{file}") as source:
        audio_data = recognizer.record(source)
        
        try:
            # Utiliser l'API Google pour reconnaître la parole
            text = recognizer.recognize_google(audio_data, language="fr-FR")
            print(f"Transcription du segment {file} terminée")
            
            # Écrire la transcription dans un fichier texte
            with open(f"./txt/{file.replace('wav', 'txt')}", 'w', encoding='utf-8') as file:
                file.write(text)
                
        except sr.UnknownValueError:
            print(f"L'API Google n'a pas pu comprendre l'audio du segment {file}.")
        except sr.RequestError as e:
            print(f"Erreur lors de la requête à l'API Google ; {e}")

os.system("rm -r temp")