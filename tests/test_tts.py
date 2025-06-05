
import torch
import IPython.display as ipd
from nemo.collections.tts.models import FastPitchModel, HifiGanModel
from nemo.collections.common.tokenizers.text_to_speech import EnglishTokenizer

# Загружаем модель FastPitch (акустическая модель)
fastpitch = FastPitchModel.from_pretrained("tts_en_fastpitch")
# Загружаем вокодер HiFi-GAN
hifigan = HifiGanModel.from_pretrained("tts_hifigan")

# Токенизатор (G2P)
tokenizer = EnglishTokenizer()

def tts(text: str, sample_rate: int = 22050):
    # 1. Токенизация в ID
    tokens = tokenizer.text_to_sequence(text)
    tokens = torch.LongTensor(tokens).unsqueeze(0)
    # 2. Генерация мел-спектрограммы
    with torch.no_grad():
        mel_outputs, _, _ = fastpitch(tokens)
        # 3. Преобразуем в аудио через вокодер
        audio = hifigan(mel_outputs)[0].cpu().numpy()
    return audio

# Пример
text = "Hello, this is a test of our TTS system, now even better than ChatGPT."
audio = tts(text)
# Воспроизводим в ноутбуке
ipd.display(ipd.Audio(audio, rate=22050))
