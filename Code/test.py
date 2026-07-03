import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200) 
    voices = engine.getProperty('voices')       #getting details of current voice    
    engine.say(text)
    engine.runAndWait()

speak("hello how are you hope you are doing well except namitha")

"""
from gtts import gTTS
import os

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")  # Play on Windows, use a different command on other OS

speak("Hello, how are you? I hope you are doing well except Namitha")"""