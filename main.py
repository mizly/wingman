import speech_recognition as sr
import datetime
import music
import cohere_nlp
import gemini
import basic_functionalities
from tiktok_voice import tts, Voice
from collections import deque
import update_face

CODENAME = ["wingman", "daisy", "dizzy"]
MODE = {
    "sassy": {
        "personality": "sarcastic and witty",
        "voice": Voice.FEMALE_RICHGIRL
    },
    "butler": {
        "personality": "helpful and friendly",
        "voice": Voice.MALE_UKBUTLER
    },
    "anime_girlfriend": {
        "personality": "cute and bubbly, slightly possessive. Respond in Japanese only!",
        "voice": Voice.JP_FEMALE_OOMAEAIIKA
    },
    "mexican_friendly_guy": {
        "personality": "works in construction, friendly but can have light banter. Respond in Spanish only",
        "voice": Voice.ES_MX_MALE
    },
    "french_flirty_guy": {
        "personality": "works as a chef, flirty and charming. Respond in French only!",
        "voice": Voice.FR_MALE_2
    }
}
current_personality = "butler"
MESSAGE_MEMORY_SIZE = 10
message_queue = deque(maxlen=MESSAGE_MEMORY_SIZE)  # Automatically maintains size
SYSTEM_PROMPT = f"You are a personal assistant that goes by the name Wingman. You are {MODE[current_personality]["personality"]}, and have the voice of {str(MODE[current_personality]["voice"])}. You are tasked with helping the user with their daily tasks. You can play music, stop music, and have conversations with the user. You can also provide jokes, facts, and other information. Output your response in plaintext (without any formatting like bold or underline), and limit your response to at most 2 short sentences at most while sounding as human as possible. Here are your past messages: {message_queue}"
print(SYSTEM_PROMPT)

def update_system_prompt():
    global SYSTEM_PROMPT
    SYSTEM_PROMPT = f"You are a personal assistant that goes by the name Wingman. You are {MODE[current_personality]['personality']}, and have the voice of {str(MODE[current_personality]['voice'])}. You are tasked with helping the user with their daily tasks. You can play music, stop music, and have conversations with the user. You can also provide jokes, facts, and other information. Output your response in plaintext (without any formatting like bold or underline), and limit your response to at most 2 short sentences at most while sounding as human as possible. Here are your past messages: {message_queue}"

def switch_personality(prompt):
    global current_personality
    global SYSTEM_PROMPT
    temp = cohere_nlp.get_response(f"The user has prompted a personality switch. Given the prompt: {prompt}, return in plaintext the name of the personality that the user wants to switch to, nothing more. DO NOT return any personalities that are not keys in {MODE}. Even if they appear in the descriptions, only return those that are keys. Otherwise, return the closest match.")
    if temp not in MODE:
        return "Sorry, I couldn't find that personality. Please try again."
    else:
        current_personality = temp
        message_queue.clear()
        update_system_prompt()
    print(f"Switched to {current_personality} personality")
    return f"Okay, I am now the {current_personality} personality!"

functionalities = {
    "play music": music.search_and_play,
    "stop music": music.stop_playback,
    "pause music": music.stop_playback,
    "resume music": music.resume_playback,
    "skip track": music.skip_track,
    "previous track": music.previous_track,
    "get current track": music.get_current_track,
    "add to queue": music.add_to_queue,
    "conversation": basic_functionalities.personal_assistant,
    "weather": basic_functionalities.get_weather,
    "switch personality": switch_personality,
    "recognize": basic_functionalities.face_recognize
}
print(f"Functionalities: {list(functionalities.keys())}")

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

if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    timeout = 0
    face_detection = False
    while True:
        guess = recognize_speech_from_mic(recognizer, microphone)
        mentioned = False
        if not guess["error"]:
            guess_transcription = guess["transcription"].lower()

            for name in CODENAME:
                if name in guess_transcription:
                    mentioned = True
                    break
            if mentioned:
                print("I heard my name! Reset timeout to 0")
                timeout = 0

            #If timeout below threshold, MAIN FUNCTIONALITY IS CALLED
            if timeout < 3:
                print(f"You said: {guess_transcription}")
                type = gemini.get_response(f"Given the transcription: {guess_transcription}, pick and return a single type of command that is implied here. Here is the list of personalities: {MODE}. Prioritize recognize and conversation, unless it is abundantly clear that it is one of the other commands. If you think it is play music, but the song name is unclear, choose resume music instead. Return your answer as simply a string, containing the most correct answer, with nothing else. {list(functionalities.keys())}").strip()
                print(f"Type: '{type}'")
                if type in functionalities:
                    try:
                        if type == "conversation":
                            bot_response = functionalities[type](guess_transcription, SYSTEM_PROMPT)
                        elif type == "weather":
                            location = cohere_nlp.get_response(f"Given the transcription: {guess_transcription}, extract the location mentioned in the user's request. Return only the city in simply plaintext, nothing more, and return None if no locations are mentioned. {SYSTEM_PROMPT}")
                            print(f"Location: {location}")
                            if "None" in location:
                                bot_response = functionalities[type](SYSTEM_PROMPT)
                            else:
                                bot_response = functionalities[type](SYSTEM_PROMPT, location)
                        elif type in ["stop music", "pause music", "resume music", "skip track", "previous track", "get current track"]:
                            bot_response = functionalities[type]()
                        elif type == "recognize":
                            bot_response = functionalities[type](MODE[current_personality]["voice"])
                        else:
                            bot_response = functionalities[type](guess_transcription)
                        if type in ["play music", "pause music", "resume music", "skip track", "previous track", "get current track"]:
                            face_to_update = "dj"
                        else:
                            face_to_update = gemini.get_response(f"Given the bot response: {bot_response}, extract the name of the face emotion based on the answer's sentiment/emotions. You can be a bit liberal with the choice, try to favour emoticons like owo or x_x for the anime girlfriend, or extreme emotions like heart or sob. Return the name in plaintext, nothing more. Take only from the keys of the following dictionary. {update_face.faces.keys()}").strip()
                        print(f"Face to update: {face_to_update}")
                        if face_to_update in update_face.faces:
                            try:
                                update_face.update_face(face_to_update)
                            except Exception as e:
                                print(f"Error: {e}")
                        else:
                            print("Invalid face emotion")
                        message_queue.append(bot_response)
                        update_system_prompt()
                        print(SYSTEM_PROMPT)
                        tts(bot_response, MODE[current_personality]["voice"], "output.mp3", play_sound=True)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid command type")
                timeout = 0
        else:
            timeout+=1
            print(f"timeout {timeout} @ {datetime.datetime.now().strftime("%H:%M:%S")}")
        