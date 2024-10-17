import speech_recognition as sr
from pydub import AudioSegment
import os

# Charger le fichier audio
audio_path = "./record/Enregistrement.wav"  # Remplacer par le chemin de votre fichier audio
text_path = audio_path.replace("record", "txt").replace(".wav", ".txt")
audio = AudioSegment.from_file(audio_path)

# Convertir en format wav si nécessaire (si c'est déjà wav, cette étape est optionnelle)
audio.export("temp_audio.wav", format="wav")

# Créer un objet Recognizer
recognizer = sr.Recognizer()

# Ouvrir le fichier audio converti en wav
with sr.AudioFile("temp_audio.wav") as source:
    audio_data = recognizer.record(source)
    
    try:
        # Utiliser l'API Google pour reconnaître la parole
        text = recognizer.recognize_google(audio_data, language="fr-FR")
        print("Transcription terminée")
        
        # Écrire la transcription dans un fichier texte
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(text)
            
    except sr.UnknownValueError:
        print("L'API Google n'a pas pu comprendre l'audio.")
    except sr.RequestError as e:
        print(f"Erreur lors de la requête à l'API Google ; {e}")

os.remove("temp_audio.wav")  # Supprimer le fichier temporaire