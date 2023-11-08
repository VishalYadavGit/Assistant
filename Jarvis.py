import speech_recognition as sr
import requests
import pyttsx3

# Initialize the SpeechRecognition recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000
# Initialize the pyttsx3 text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process user's voice input
def process_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Use Google Speech Recognition to convert speech to text
        query = recognizer.recognize_google(audio)
        print(f"User: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, I couldn't reach the speech recognition service.")
        return ""

# Function to send the user's input to the OpenAI GPT-3 API and get a response
def get_chatbot_response(input_text):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = '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'

    # Define the OpenAI GPT-3 API endpoint
    api_endpoint = 'https://api.openai.com/v1/completions'

    # Set the GPT-3 parameters
    payload = {
        'prompt': input_text,
        'max_tokens': 100,
        'temperature': 0.7
    }

    # Set the request headers with the API key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        # Send a POST request to the OpenAI GPT-3 API
        response = requests.post(api_endpoint, json=payload, headers=headers)
        response.raise_for_status()

        # Parse the response JSON
        response_json = response.json()

        # Extract the generated chatbot response
        chatbot_response = response_json['choices'][0]['text'].strip()

        return chatbot_response
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        return ""

# Main loop to continuously listen for voice input and provide voice output
while True:
    # Listen for voice input and convert it to text
    user_input = process_voice_input()

    if user_input.lower() == 'exit':
        # If the user says 'exit', end the program
        speak("Goodbye!")
        break

    if user_input:
        # Send user's input to the OpenAI GPT-3 API and get a response
        chatbot_response = get_chatbot_response(user_input)

        if chatbot_response:
            # Convert the chatbot's response to voice output
            speak(chatbot_response)
        else:
            speak("Sorry, I couldn't generate a response.")




