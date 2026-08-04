from transformers import pipeline


# "automatic-speech-recognition" is Hugging Face's task name for speech-to-text.
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base")


def transcribe_audio(file_path: str) -> str:
    """Given a path to an audio file, return the transcribed text."""
    #looks at string as an address, opens file at address and reads the raw bytes into memory 
    result = transcriber(file_path)



    #returns a dictionary, but we only want the transcribed text
    return result["text"]