import cv2
import gemini
import requests
import json
import time
import mediapipe as mp
import facerec
from tiktok_voice import tts, Voice
import speech_recognition as sr
import datetime
import cohere_nlp
# API Key
with open("config.json") as f:
    config = json.load(f)

WEATHER_API_KEY = config.get("WEATHER_API_KEY")

def get_weather(SYSTEM_PROMPT, LOCATION="Toronto"):
    API_URL = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={LOCATION}&aqi=no"
    # Make the API request
    response = requests.get(API_URL)
    SYSTEM_PROMPT = "You are a personal assistant that goes by the name Wingman. You are helpful and friendly, and have the voice of Voice.MALE_UKBUTLER. You are tasked with helping the user with their daily tasks. You can play music, stop music, and have conversations with the user. You can also provide jokes, facts, and other information. Output your response in plaintext (without any formatting like bold or underline), and limit your response to at most 2 short sentences at most while sounding as human as possible. Here are your past messages: deque([], maxlen=5)"
    if response.status_code == 200:
        json_response = response.json()  # Store the JSON response
        location = json_response["location"]
        current_weather = json_response["current"]
        
        # Extracting relevant details
        city = location["name"]
        country = location["country"]
        temp_c = current_weather["temp_c"]
        
        weather_report = f"The weather in {city}, {country} is {int(temp_c)} degrees."
        bot_response = gemini.get_response(f"Provide the user with the current weather and a general description of the weather (you could use the windchill values, humidity, etc.. anything else you may think helpful). {SYSTEM_PROMPT}. Your rsponse should start with {weather_report}")
        print(bot_response)
        return bot_response
    else:
        return "I couldn't get the weather for you."

def personal_assistant(text, system_prompt):
    return gemini.get_response(f"{system_prompt}. Here is the user prompt: {text}")

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def face_recognize(voice):
    cap = cv2.VideoCapture(0)
    
    mp_face_detection = mp.solutions.face_detection
    #mp_drawing = mp.solutions.drawing_utils
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    face_detected = False
    detected_time = 0
    max_time = 2
    start_time = time.time()
    

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image_rgb)

        if results.detections:
            if not face_detected:
                face_detected = True
                detected_time = time.time()
            elif time.time() - detected_time > max_time:
                break  # Exit loop once face detection is confirmed for max_time
        else:
            if face_detected:
                face_detected = False
                break  # Exit loop when no face is detected
            elif time.time() - start_time > max_time:
                break



    #here face is guaranteed to be detected or not.
    if not face_detected:
        return "I don't see a face right now"

    recog = facerec.faceRecog(image)
    if(recog!=False):
        return "Hello "+recog+"! Nice to see you again!"
    
    tts("I don't recognize you, so let's add your face! What's your name?", voice, "output.mp3", play_sound=True)
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    timeout = 0
    name = "none"
    while timeout<3:
        guess = recognize_speech_from_mic(recognizer, microphone)
        if not guess["error"]:
            guess_transcription = guess["transcription"].lower()
            print(f"You said: {guess_transcription}")
            name = cohere_nlp.get_response(f"The user's prompt was {guess_transcription}. Return just the name if a person's name is detected, otherwise return None. Make sure your response is a single word in plaintext.")
            print(name)
            if name.lower() != "none":
                break
            else:
                tts("Could you try again? What's your name?", voice, "output.mp3", play_sound=True)
        else:
            timeout+=1
            print("timeout " + str(timeout) + " @ " + datetime.datetime.now().strftime("%H:%M:%S"))
    if name.lower() == "none":
        return("Sorry, I couldn't get your name. Maybe let's try again later?")

    facerec.addFace(name, image)
    cap.release()
    cv2.destroyAllWindows()
    return f"Welcome, {name}!"

