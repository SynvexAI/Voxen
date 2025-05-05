import os
from trainer import Trainer, TrainerArgs
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.configs.shared_configs import BaseDatasetConfig

if __name__ == "__main__":
    # Путь к директории с проектом
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Создаём объекты конфигурации
    dataset_config = BaseDatasetConfig(
        name="MyDataset",
        path=os.path.join(project_dir, "../data"),
        formatter="ljspeech",
        meta_file_train="metadata.csv"
    )

    # Загружаем параметры из JSON
    config = VitsConfig.from_json(os.path.join(project_dir, "../configs/config.json"))
    config.datasets = [dataset_config]  # Подставляем наш датасет

    # Запуск обучения
    trainer = Trainer(config)
    trainer.fit()
