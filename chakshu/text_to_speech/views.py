from .nix_tts import TextToSpeech


def convert_text_to_speech(text, output_file=None):
    tts = TextToSpeech()
    audio_bytes = tts.text_to_speech(text, output_file=output_file)

    if output_file is not None:
        with open(output_file, "rb") as f:
            audio_bytes = f.read()

    return audio_bytes
