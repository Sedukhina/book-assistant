from gtts import gTTS

def text_to_speech_ukrainian(text, output_path='static/response.mp3'):
    """
    Конвертує текст у мову за допомогою Google TTS та зберігає файл.
    """
    try:
        tts = gTTS(text, lang='uk')  # 'uk' для української мови
        tts.save(output_path)
        return output_path
    except Exception as e:
        return f"Помилка: {e}"
