import speech_recognition as sr
from googletrans import Translator
# import pyttsx3

import pygame.mixer

import requests
import json
import io

from speech_recognition import UnknownValueError

# Initialize the speech recognizer
r = sr.Recognizer()

# Initialize the translator
translator = Translator()

# Initialize the text-to-speech engine
# engine = pyttsx3.init()


def text_to_speech(text):
      #11,-male
    #2-female
    # 69-child
    speaker_id = 2 # Choose the appropriate speaker_id based on your requirement
    params=(("text",text),
            ("speaker",speaker_id),
            ("postPhonemeLength", 1.0),
            ("prePhonemeLength", 1.0),
            ("intonationScale", 1.5),
            ("speedScale", 1.7),
            ("volumeScale", 4.0)
            )

    response = requests.post("http://127.0.0.1:50021/audio_query",params=params )
    res=requests.post("http://127.0.0.1:50021/synthesis",
                    headers={"Content-Type":"application/json"},
                    params=params,
                    data=json.dumps(response.json()))

    audio = io.BytesIO(res.content)

    # Load the audio into a Sound object
    sound = pygame.mixer.Sound(audio)

    # Play the audio
    sound.play()

    # Wait for the audio to finish playing
    pygame.time.wait(int(sound.get_length() * 1000))

     

# Function to record and translate voice
def record_and_translate():
    while True:
            with sr.Microphone() as source:
                print("Speak something...")
                audio = r.listen(source)
                print("Recording finished.")

            try:  # Convert speech to text
                text = r.recognize_google(audio)
            except UnknownValueError:
                print("Sorry, I could not understand the audio.")
                continue

            # Translate the text
            translation = translator.translate(text, dest='ja')
            print(f'Translated text: {translation.text}')

            # Convert translated text to speech
            text_to_speech(translation.text)

            # engine.say(translation.text)
            # engine.runAndWait()

# Call the function to record and translate voice
# output_language = input("Enter the language you want to translate to... en for english, ja for japaneese: ")

record_and_translate()  