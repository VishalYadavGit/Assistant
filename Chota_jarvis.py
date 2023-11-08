import google.generativeai as palm
import speech_recognition as sr
import pyttsx3


recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000

while True:
    with sr.Microphone() as source:
        print("Speak something... press CRL+C to STOP")
        audio = recognizer.listen(source)

    try:
        # Use the Google Web Speech API to recognize the audio
        text = recognizer.recognize_google(audio)
        print(text)
        api_key = 'AIzaSyC4aAAy1jo_SnmIEDMUpDbMVeS70n_mq2s'
        palm.configure(api_key=api_key)
        response = palm.chat(messages=[text])
        print(response.last) #  'Hello! What can I help you with?'
        engine = pyttsx3.init()
        say = response.last
        engine.say(say)
        engine.runAndWait()
        
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
