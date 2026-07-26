from transformers import pipeline 




summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn12-6")




def summarize_text(text: str) -> str: 
    """Given raw text, return an AI-generated summary"""
    result = summarizer(text, max_length=100, min_length=20, do_sample=False)
    return result[0]["summary_text"]
