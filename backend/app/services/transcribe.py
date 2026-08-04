from transformers import pipeline


# First run downloads ~150MB from Hugging Face into ~/.cache/huggingface/
# Subsequent runs read from cache — fast.
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")


def transcribe_audio(file_path: str) -> str:
    """Given a path to an audio file, return the transcribed text."""
    result = transcriber(file_path)
    return result["text"]