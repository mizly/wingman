import speech_recognition as sr
import datetime
import music
import nlp
import basic_functionalities
from tiktok_voice import tts, Voice
from collections import deque

CODENAME = ["wingman", "daisy", "dizzy"]
MODE = {
    "dizzy": {
        "personality": "sarcastic and witty",
        "voice": Voice.FEMALE_RICHGIRL
    },
    "wingman": {
        "personality": "helpful and friendly",
        "voice": Voice.MALE_UKBUTLER
    }
}
current_personality = "wingman"
MESSAGE_MEMORY_SIZE = 5
message_queue = deque(maxlen=MESSAGE_MEMORY_SIZE)  # Automatically maintains size
SYSTEM_PROMPT = f"You are a personal assistant that goes by the name Wingman. You are {MODE[current_personality]["personality"]}, and have the voice of {str(MODE[current_personality]["voice"])}. You are tasked with helping the user with their daily tasks. You can play music, stop music, and have conversations with the user. You can also provide jokes, facts, and other information. Output your response in plaintext (without any formatting like bold or underline), and limit your response to at most 2 short sentences at most while sounding as human as possible. Here are your past messages: {message_queue}"
print(SYSTEM_PROMPT)
functionalities = {
    "play music": music.search_and_play,
    "stop music": music.stop_playback,
    "resume music": music.resume_playback,
    "skip track": music.skip_track,
    "previous track": music.previous_track,
    "get current track": music.get_current_track,
    "add to queue": music.add_to_queue,
    "conversation": basic_functionalities.personal_assistant
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

    while True:
        # get the speech from the user
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

            #If timeout < 5, MAIN FUNCTIONALITY IS CALLED
            if timeout < 3:
                print(f"You said: {guess_transcription}")
                type = nlp.get_response(f"Given the transcription: {guess_transcription}, pick and return a single type of command that is implied here. Prioritize conversation, unless it is abundantly clear that it is one of the other commands. If you think it is play music, but the song name is unclear, choose resume music instead. Return your answer as simply a string, containing the most correct answer, with nothing else. {list(functionalities.keys())}")
                print(f"Type: {type}")
                if type in functionalities:
                    try:
                        if type == "conversation":
                            bot_response = functionalities[type](guess_transcription, SYSTEM_PROMPT)
                            message_queue.append(bot_response)
                        else:
                            bot_response = functionalities[type](guess_transcription)
                        tts(bot_response, MODE[current_personality]["voice"], "output.mp3", play_sound=True)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid command type")
                timeout = 0
        else:
            timeout+=1
            print(f"timeout {timeout} @ {datetime.datetime.now().strftime("%H:%M:%S")}")
        
