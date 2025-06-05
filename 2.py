# В терминале (или командной строке) сначала установите библиотеку:
# pip install TTS

from TTS.api import TTS
import random

def insert_disfluencies(text, rate=0.1):
    """
    Вставляет запинки (дизфлюенции) в текст с указанной вероятностью.
    Например, после каждого слова с вероятностью rate добавляется один из вариантов: и..., эм..., ы... и т.п.
    """
    words = text.split()
    new_words = []
    disfluencies = ["и...", "эм...", "ы...", "э..."]
    for word in words:
        new_words.append(word)
        if random.random() < rate:
            new_words.append(random.choice(disfluencies))
    return " ".join(new_words)

def synthesize(text, output_path="output.wav"):
    """
    Синтезирует речь из текста с добавлением запинок и сохраняет результат в указанный файл.
    """
    # Загружаем предобученную модель для русского языка
    tts = TTS(model_name="tts_models/ru/vkt/vits")
    
    # Вставляем запинки
    processed_text = insert_disfluencies(text)
    
    # Генерируем аудиофайл
    tts.tts_to_file(text=processed_text, file_path=output_path)
    print(f"Синтез завершён. Файл сохранён как {output_path}")

if __name__ == "__main__":
    # Запросим у пользователя текст для синтеза
    text = input("Введите текст для синтеза: ")
    synthesize(text)
