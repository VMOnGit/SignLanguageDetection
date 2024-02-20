import pyttsx3
def speak(text):
    engine = pyttsx3.init() # object creation
    engine.setProperty('voice', 1)
    engine.say(text)
    engine.runAndWait()
    engine.stop()