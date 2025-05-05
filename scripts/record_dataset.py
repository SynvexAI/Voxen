import sounddevice as sd
import soundfile as sf

fs = 22050  # частота дискретизации
data_dir = "data/raw"  # папка для сохранения

# Список фраз для записи (пример). Замените своими фразами или загрузите из текстового файла.
sentences = [
    "Привет, как дела?",
    "Скажите это предложение через секунду.",
    "Сегодня хорошая погода.",
    "Человек счастлив, когда он говорит правду.",
    "Искусственный интеллект развивается быстро."
]

print("Запись начнётся после нажатия Enter.")
for i, text in enumerate(sentences, start=1):
    input(f"\nНажмите Enter и произнесите фразу: \"{text}\"")
    print("Записываю...")
    recording = sd.rec(int(5 * fs), samplerate=fs, channels=1)  # записываем 5 секунд
    sd.wait()
    filename = f"{i:04d}.wav"
    sf.write(f"{data_dir}/{filename}", recording, fs)
    print(f"Сохранено {data_dir}/{filename}")
