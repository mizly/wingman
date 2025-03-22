from tiktok_voice import tts, Voice

if __name__ == "__main__":
    text = '안녕하세요 여러분, 저는 코딩하는 개발자입니다.'
    tts(text, Voice.KR_FEMALE, "output.mp3", play_sound=True)