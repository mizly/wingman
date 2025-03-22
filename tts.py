from tiktok_voice import tts, Voice

if __name__ == "__main__":
    text = 'hi bro'
    tts(text, Voice.MALE_UKBUTLER, "output.mp3", play_sound=True)