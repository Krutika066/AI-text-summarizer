import requests
import os
from rake_nltk import Rake
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq

# Download necessary NLTK data
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('punkt_tab')

class AISummarizer:
    def __init__(self):
        # Use Hugging Face Inference API
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        # The token should be set in environment variables for security
        self.api_token = os.getenv("HF_API_TOKEN", "") 
        self.rake = Rake()
        print("AI Summarizer initialized")

    def summarize(self, text, length_type="medium"):
        """
        Summarizes text using the Hugging Face Inference API if token exists, 
        otherwise falls back to a local extractive summarizer.
        """
        if not self.api_token:
            print("WARNING: HF_API_TOKEN not found. Using local extractive fallback.")
            return self.local_summarize(text, length_type)

        # Determine parameters based on length_type
        text_length = len(text.split())
        if length_type == "short":
            max_l, min_l = min(50, text_length // 2), 10
        elif length_type == "long":
            max_l, min_l = min(400, text_length // 1.5), 100
        else:
            max_l, min_l = min(150, text_length // 2), 50

        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "inputs": text,
            "parameters": {"max_length": max_l, "min_length": min_l, "do_sample": False}
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            result = response.json()
            
            # The API sometimes returns a list or a dict with error
            if isinstance(result, list) and len(result) > 0:
                summary_text = result[0].get('summary_text', "No summary generated.")
            elif 'error' in result:
                # If API error (like overloaded), fallback to local
                print(f"API Error: {result['error']}. Falling back to local.")
                return self.local_summarize(text, length_type)
            else:
                summary_text = "Unexpected API response format."
                
            keywords = self.extract_keywords(text)
            return summary_text, keywords
            
        except Exception as e:
            print(f"Summarization API Error: {e}. Falling back to local.")
            return self.local_summarize(text, length_type)

    def local_summarize(self, text, length_type="medium"):
        """A simple frequency-based extractive summarizer as a fallback."""
        try:
            stop_words = set(stopwords.words('english'))
            words = word_tokenize(text.lower())
            
            # Calculate word frequencies
            freq_table = {}
            for word in words:
                if word.isalnum() and word not in stop_words:
                    freq_table[word] = freq_table.get(word, 0) + 1
            
            # Normalize frequencies
            if not freq_table:
                return text[:200] + "...", self.extract_keywords(text)
                
            max_freq = max(freq_table.values())
            for word in freq_table:
                freq_table[word] = freq_table[word] / max_freq
            
            # Score sentences
            sentences = sent_tokenize(text)
            sent_scores = {}
            for sent in sentences:
                for word, freq in freq_table.items():
                    if word in sent.lower():
                        sent_scores[sent] = sent_scores.get(sent, 0) + freq
            
            # Determine number of sentences based on length_type
            if length_type == "short":
                num_sents = max(1, len(sentences) // 4)
            elif length_type == "long":
                num_sents = max(3, len(sentences) // 2)
            else:
                num_sents = max(2, len(sentences) // 3)
            
            # Get top sentences
            summary_sentences = heapq.nlargest(num_sents, sent_scores, key=sent_scores.get)
            
            # Reorder sentences as they appear in original text
            final_sentences = [s for s in sentences if s in summary_sentences]
            summary_text = " ".join(final_sentences)
            
            # Add a prefix to let user know it's a fallback
            prefix = "[Local Fallback Summary] "
            keywords = self.extract_keywords(text)
            
            return prefix + summary_text, keywords
        except Exception as e:
            print(f"Local Summarization Error: {e}")
            return text[:200] + "...", self.extract_keywords(text)

    def extract_keywords(self, text, num_keywords=5):
        """Extracts top keywords from the text."""
        try:
            self.rake.extract_keywords_from_text(text)
            return self.rake.get_ranked_phrases()[:num_keywords]
        except:
            return []

# Singleton instance
ai_summarizer = AISummarizer()
