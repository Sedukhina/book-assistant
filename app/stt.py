import os
from speech_recognition import Recognizer, Microphone

def record_and_recognize():
    """
    Записує голос із мікрофона та розпізнає текст.
    """
    recognizer = Recognizer()
    
    try:
        # Виводимо список доступних мікрофонів
        print("Доступні мікрофони:", Microphone.list_microphone_names())
        
        with Microphone() as source:
            # Налаштування рівня шуму (опціонально для покращення розпізнавання)
            print("Налаштування рівня шуму. Зачекайте...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print("Скажіть щось...")
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
            
            print("Розпізнавання...")
            text = recognizer.recognize_google(audio, language='uk-UA')
            
            print(f"Розпізнаний текст: {text}")
            return text
    
    except Exception as e:
        print(f"Помилка запису або розпізнавання: {e}")
        return "Помилка запису або розпізнавання."
