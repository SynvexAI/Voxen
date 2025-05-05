import glob
import os
import soundfile as sf
import numpy as np

input_dir = "data/raw"
output_dir = "data/normalized"
os.makedirs(output_dir, exist_ok=True)

files = glob.glob(f"{input_dir}/*.wav")
for wav_path in files:
    data, sr = sf.read(wav_path)
    # Находим максимальную амплитуду
    peak = np.max(np.abs(data))
    if peak == 0:
        continue
    # Масштабируем так, чтобы пиковое значение стало 0.99
    normalized = data / peak * 0.99
    out_path = os.path.join(output_dir, os.path.basename(wav_path))
    sf.write(out_path, normalized, sr)
    print(f"Нормализован {out_path}")
