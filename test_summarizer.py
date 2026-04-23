from transformers import pipeline
print("Loading summarizer...")
try:
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print("Summarizer loaded!")
    text = "The quick brown fox jumps over the lazy dog. This is a test sentence for summarization."
    result = summarizer(text, max_length=10, min_length=5, do_sample=False)
    print("Result:", result)
except Exception as e:
    print("Error:", e)
