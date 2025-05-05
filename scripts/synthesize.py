from TTS.api import TTS
import os

# Указываем пути к модели и конфигу
model_path = "output/best_model.pth"      # файл с обученной моделью
config_path = "output/config.json"        # файл конфигурации
# Если у вас использовался внешний вокодер, укажите paths на vocoder тоже

# Инициализация модели TTS
tts = TTS(model_path=model_path, config_path=config_path)

# Текст для синтеза
text = "Это пример синтеза речи с помощью обученной модели."

# Синтез в аудиофайл
output_wav = "output/output.wav"
tts.tts_to_file(text=text, file_path=output_wav)
print(f"Синтез завершён. Файл: {output_wav}")
