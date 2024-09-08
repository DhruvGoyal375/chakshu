import io
import os

import gdown
import numpy as np
import scipy.io.wavfile as wav
from nix.models.TTS import NixTTSInference


class TextToSpeech:
    def __init__(self, model_dir="text_to_speech/nix-ljspeech-deterministic-v0.1"):
        self.model_dir = model_dir
        self.file_urls = {
            "decoder.onnx": "https://drive.google.com/uc?id=1NahMOHe39Q8Miup9iGJSGgKK5r54Dy7t",
            "encoder.onnx": "https://drive.google.com/uc?id=1vsp8oqdFvQahODc2xax6JAUPWl9tmBzt",
            "tokenizer_state.pkl": "https://drive.google.com/uc?id=1BqN4qdIpswIJ-S8E7ZO70W5p9am1wPDy",
        }
        self.ensure_model()
        self.nix = NixTTSInference(model_dir=self.model_dir)

    def ensure_model(self):
        if not os.path.exists(self.model_dir):
            print("Model not found. Downloading...")
            os.makedirs(self.model_dir, exist_ok=True)
            self.download_files()
        else:
            print("Model is already downloaded")

    def download_files(self):
        for file_name, url in self.file_urls.items():
            file_path = os.path.join(self.model_dir, file_name)
            if not os.path.exists(file_path):
                print(f"Downloading {file_name}...")
                gdown.download(url, file_path, quiet=False)
            else:
                print(f"{file_name} already exists.")

    def text_to_speech(self, text, output_file=None):
        c, c_length, _ = self.nix.tokenize(text)
        xw = self.nix.vocalize(c, c_length)

        audio_data = xw[0, 0].astype(np.float32)
        sample_rate = 16000

        if output_file:
            wav.write(output_file, sample_rate, audio_data)
            print(f"Audio has been saved to {output_file}")
            return None
        else:
            buffer = io.BytesIO()
            wav.write(buffer, sample_rate, audio_data)
            audio_bytes = buffer.getvalue()
            return audio_bytes


if __name__ == "__main__":
    tts = TextToSpeech()
    tts.text_to_speech("1. Born to multiply, born to gaze into night skies.")
