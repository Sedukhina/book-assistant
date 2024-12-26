import os
from speech_recognition import Recognizer, Microphone

def record_and_recognize():
    """
    Записує голос із мікрофона та розпізнає текст.
    """
    recognizer = Recognizer()
    try:
        with Microphone() as source:
            print("Скажіть щось...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("Розпізнавання...")
            return recognizer.recognize_google(audio, language='uk-UA')
    except Exception as e:
        return f"Помилка розпізнавання: {e}"
