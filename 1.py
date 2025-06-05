import random
import wave
import os
# Убедитесь, что piper установлен: pip install piper-tts
# Если piper не импортируется, значит, он не установлен в вашем окружении Python.
try:
    from piper import PiperVoice
except ImportError:
    print("Библиотека piper не найдена. Пожалуйста, установите ее: pip install piper-tts")
    PiperVoice = None # Для предотвращения ошибок ниже, если piper не установлен

# --- Конфигурация ---
# Путь к скачанным файлам голосовой модели Piper
MODEL_DIR = './model/' # Создайте эту папку и поместите туда файлы модели
# Замените на имя вашего файла модели, если оно другое
VOICE_MODEL_FILENAME_STEM = 'ru_RU-irina-medium'
VOICE_ONNX = os.path.join(MODEL_DIR, f'{VOICE_MODEL_FILENAME_STEM}.onnx')
VOICE_JSON = os.path.join(MODEL_DIR, f'{VOICE_MODEL_FILENAME_STEM}.onnx.json')
OUTPUT_WAV_PATH = 'output_hesitated.wav'

# --- Функция для добавления запинок ---
def add_hesitations(text, probability=0.15):
    """
    Добавляет слова-запинки в текст.
    probability: вероятность добавления запинки после слова (от 0 до 1).
    """
    words = text.split(' ')
    # Вы можете расширить этот список
    hesitations = ["эм...", "э-э...", "ну...", "типа...", "как бы...", "ы-ы...", "значит..."]
    new_sentence_parts = []
    
    for word in words:
        new_sentence_parts.append(word)
        # Добавляем запинку, если выпал шанс и слово не заканчивается знаком пунктуации
        if random.random() < probability and not any(punc in word for punc in ['.', ',', '!', '?']):
            new_sentence_parts.append(random.choice(hesitations))
            
    return ' '.join(new_sentence_parts)

# --- Основная функция синтеза речи ---
def text_to_speech_with_hesitations(text_to_speak):
    if PiperVoice is None:
        print("PiperVoice не инициализирован (возможно, piper-tts не установлен). Синтез невозможен.")
        return

    print(f"Оригинальный текст: {text_to_speak}")
    
    # 1. Добавляем запинки
    text_with_hesitations = add_hesitations(text_to_speak)
    print(f"Текст с запинками: {text_with_hesitations}")
    
    # 2. Синтезируем речь с помощью Piper
    if not (os.path.exists(VOICE_ONNX) and os.path.exists(VOICE_JSON)):
        print(f"ОШИБКА: Файлы голосовой модели не найдены в '{MODEL_DIR}'.")
        print(f"Пожалуйста, скачайте '{os.path.basename(VOICE_ONNX)}' и '{os.path.basename(VOICE_JSON)}'")
        print(f"Например, отсюда: https://huggingface.co/rhasspy/piper-voices/tree/main/ru/ru_RU/irina/medium")
        print(f"И поместите их в папку '{MODEL_DIR}' в текущей директории.")
        return

    print("Загрузка голосовой модели...")
    try:
        voice = PiperVoice.load(VOICE_ONNX, VOICE_JSON)
    except Exception as e:
        print(f"Ошибка загрузки модели Piper: {e}")
        print("Убедитесь, что у вас правильные файлы модели и piper-tts установлен корректно.")
        return

    print(f"Синтез аудио в файл {OUTPUT_WAV_PATH}...")
    try:
        # Piper синтезирует аудиоданные, которые нужно записать в WAV файл
        # synthesize_stream можно использовать для потоковой записи, если нужно
        audio_data = voice.synthesize(text_with_hesitations) # Возвращает итератор аудио чанков

        with wave.open(OUTPUT_WAV_PATH, 'wb') as wav_file:
            # Параметры WAV файла должны соответствовать выводу модели Piper
            # Обычно это: 1 канал, 2 байта на сэмпл (16 бит), частота дискретизации (например, 22050 Гц для многих моделей)
            # Эти параметры можно получить из voice.config
            wav_file.setnchannels(voice.config.num_channels if voice.config.num_channels else 1) # type: ignore
            wav_file.setsampwidth(voice.config.sample_width if voice.config.sample_width else 2) # type: ignore
            wav_file.setframerate(voice.config.sample_rate if voice.config.sample_rate else 22050) # type: ignore
            
            for chunk in audio_data:
                wav_file.writeframes(chunk)
                
        print(f"Аудио успешно сохранено в {OUTPUT_WAV_PATH}")
        print("Теперь вы можете воспроизвести этот файл любым аудиоплеером.")
        
        # Опционально: попытка воспроизвести файл (требует playsound или другую библиотеку)
        # try:
        #     from playsound import playsound
        #     print("Воспроизведение аудио...")
        #     playsound(OUTPUT_WAV_PATH)
        # except ImportError:
        #     print("Для автоматического воспроизведения установите 'playsound': pip install playsound")
        # except Exception as e_play:
        #     print(f"Ошибка воспроизведения звука: {e_play}")

    except Exception as e:
        print(f"Ошибка во время синтеза: {e}")

# --- Пример использования ---
if __name__ == '__main__':
    input_text = "Привет, это демонстрация работы текста с запинками и надеюсь неплохой интонацией."
    
    # Проверяем/создаем папку для модели
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"Создана папка '{MODEL_DIR}'.")
        print(f"Пожалуйста, скачайте файлы голосовой модели (например, '{VOICE_MODEL_FILENAME_STEM}.onnx' и '{VOICE_MODEL_FILENAME_STEM}.onnx.json')")
        print(f"из https://huggingface.co/rhasspy/piper-voices/tree/main/ru/ru_RU/irina/medium")
        print(f"и поместите их в папку '{MODEL_DIR}'.")
    
    # Запускаем синтез только если PiperVoice был успешно импортирован
    if PiperVoice:
        text_to_speech_with_hesitations(input_text)
    else:
        print("Не удалось запустить синтез, так как Piper TTS не был загружен.")