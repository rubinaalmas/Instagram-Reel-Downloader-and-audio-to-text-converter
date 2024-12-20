import pandas as pd
import speech_recognition as sr

def audio_to_text(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "Sorry, I'm unable to reach the speech recognition service."


audio_path = "audio_path_to_the_audio_from reel"

#audio-to-text description
audio_text = audio_to_text(audio_path)

# dataFrame 
df = pd.DataFrame({
    'number': range(1, 1001),  # Numbers from 1 to 1000
    'audio_description': [audio_text] * 1000  # Same text in all rows
})

# CSV file
df.to_csv("/Users/rubinaalmas/Downloads/audio_text_output.csv", index=False)

print("DataFrame created with 1000 rows and saved to 'audio_text_output.csv'.")
