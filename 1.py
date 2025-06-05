import random
import wave
import os
import sys # Для более информативного вывода

# --- Конфигурация ---
# Путь к папке со скачанными файлами голосовой модели Piper
MODEL_DIR = './model/' 
# Имя вашей модели (без расширения). Должно совпадать с именами скачанных файлов.
VOICE_MODEL_FILENAME_STEM = 'ru_RU-irina-medium' 
VOICE_ONNX = os.path.join(MODEL_DIR, f'{VOICE_MODEL_FILENAME_STEM}.onnx')
VOICE_JSON = os.path.join(MODEL_DIR, f'{VOICE_MODEL_FILENAME_STEM}.onnx.json')
OUTPUT_WAV_PATH = 'output_hesitated.wav'

# Попытка импорта piper-tts
try:
    from piper import PiperVoice
    PIPER_INSTALLED = True
except ImportError:
    PIPER_INSTALLED = False
    PiperVoice = None # Определяем для предотвращения ошибок ниже, если piper не установлен

# --- Функция для добавления запинок ---
def add_hesitations(text, probability=0.15):
    """
    Добавляет слова-запинки в текст.
    probability: вероятность добавления запинки после слова (от 0 до 1).
    """
    words = text.split(' ')
    # Вы можете расширить этот список или изменить существующие запинки
    hesitations = ["эм...", "э-э...", "ну...", "типа...", "как бы...", "ы-ы...", "значит..."]
    new_sentence_parts = []
    
    for word in words:
        new_sentence_parts.append(word)
        # Добавляем запинку, если выпал шанс и слово не заканчивается знаком пунктуации
        # и если это не само слово-паразит (чтобы не было "эм... эм...")
        if random.random() < probability and \
           not any(punc in word for punc in ['.', ',', '!', '?']) and \
           word.lower() not in hesitations:
            new_sentence_parts.append(random.choice(hesitations))
            
    return ' '.join(new_sentence_parts)

# --- Основная функция синтеза речи ---
def text_to_speech_with_hesitations(text_to_speak):
    if not PIPER_INSTALLED or PiperVoice is None:
        print("--------------------------------------------------------------------")
        print("ОШИБКА: Библиотека piper-tts не установлена или не может быть импортирована.")
        print("Пожалуйста, установите ее, выполнив в вашем терминале/командной строке:")
        print("  pip3 install piper-tts  (или pip install piper-tts)")
        print(f"Для интерпретатора Python: {sys.executable}")
        print("Убедитесь, что вы устанавливаете ее в то же окружение Python, где запускаете этот скрипт.")
        print("--------------------------------------------------------------------")
        return

    print(f"Оригинальный текст: {text_to_speak}")
    
    # 1. Добавляем запинки
    text_with_hesitations = add_hesitations(text_to_speak)
    print(f"Текст с запинками: {text_with_hesitations}")
    
    # 2. Проверяем наличие файлов модели
    if not (os.path.exists(VOICE_ONNX) and os.path.exists(VOICE_JSON)):
        print("--------------------------------------------------------------------")
        print(f"ОШИБКА: Файлы голосовой модели не найдены.")
        print(f"Ожидались файлы: ")
        print(f"  1. {os.path.abspath(VOICE_ONNX)}")
        print(f"  2. {os.path.abspath(VOICE_JSON)}")
        print(f"Пожалуйста, скачайте модель (например, '{VOICE_MODEL_FILENAME_STEM}') с:")
        print(f"  https://huggingface.co/rhasspy/piper-voices/tree/main/ru/ru_RU/irina/medium")
        print(f"и поместите .onnx и .onnx.json файлы в папку '{os.path.abspath(MODEL_DIR)}'.")
        if not os.path.exists(MODEL_DIR):
            try:
                os.makedirs(MODEL_DIR)
                print(f"Папка '{os.path.abspath(MODEL_DIR)}' была только что создана. Поместите в нее файлы модели.")
            except OSError as e:
                print(f"Не удалось создать папку '{os.path.abspath(MODEL_DIR)}': {e}. Создайте ее вручную.")
        print("--------------------------------------------------------------------")
        return

    print("Загрузка голосовой модели Piper...")
    try:
        voice = PiperVoice.load(model_path=VOICE_ONNX, config_path=VOICE_JSON)
    except Exception as e:
        print(f"Ошибка загрузки модели Piper: {e}")
        print("Убедитесь, что у вас правильные файлы модели и piper-tts установлен корректно.")
        print("Также проверьте, что версия piper-tts совместима с моделью (обычно проблем нет).")
        return

    print(f"Синтез аудио в файл {OUTPUT_WAV_PATH}...")
    try:
        audio_data_iterator = voice.synthesize_stream_raw(text_with_hesitations)

        with wave.open(OUTPUT_WAV_PATH, 'wb') as wav_file:
            wav_file.setnchannels(voice.config.num_channels)
            wav_file.setsampwidth(voice.config.sample_width) 
            wav_file.setframerate(voice.config.sample_rate)
            
            for audio_chunk in audio_data_iterator:
                wav_file.writeframes(audio_chunk)
                
        print(f"Аудио успешно сохранено в {os.path.abspath(OUTPUT_WAV_PATH)}")
        print("Теперь вы можете воспроизвести этот файл любым аудиоплеером.")
        
    except Exception as e:
        print(f"Ошибка во время синтеза: {e}")

# --- Пример использования ---
if __name__ == '__main__':
    input_text = "Привет, это демонстрация работы текста с запинками и, надеюсь, неплохой интонацией."
    
    if not os.path.exists(MODEL_DIR) and PIPER_INSTALLED : # Создаем папку, только если piper установлен, чтобы не создавать ее зря
        try:
            os.makedirs(MODEL_DIR)
            print(f"Создана папка для модели: '{os.path.abspath(MODEL_DIR)}'.")
            print(f"Не забудьте поместить в нее файлы .onnx и .onnx.json вашей голосовой модели.")
        except OSError as e:
            print(f"Не удалось создать папку для модели '{MODEL_DIR}': {e}. Пожалуйста, создайте ее вручную.")

    text_to_speech_with_hesitations(input_text)