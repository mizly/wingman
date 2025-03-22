import speech_recognition as sr
import datetime
import play_music
CODENAME = ["dizzy", "wingman", "daisy"]

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

            #If timeout < 3, print the transcription
            if timeout < 3:
                print(f"You said: {guess_transcription}. Current timeout: {timeout}")
        else:
            timeout+=1
            print(f"timeout {timeout} @ {datetime.datetime.now().strftime("%H:%M:%S")}")
        
