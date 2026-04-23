# SummaAI - Advanced AI Text Summarizer

A modern, full-stack web application that uses state-of-the-art NLP models to summarize long text and documents (PDF/TXT). Built with **FastAPI** and **HuggingFace Transformers**.

## ✨ Features
- **Smart Summarization**: Uses `DistilBART` for high-quality abstractive summaries.
- **Multiple Formats**: Support for manual text input and PDF/TXT file uploads.
- **Customizable Length**: Choose between Short, Medium, and Long summaries.
- **Keyword Extraction**: Automatically identifies key themes in the content.
- **Premium UI**: Modern dark-mode interface with glassmorphism and animations.
- **Utilities**: Copy to clipboard and download summary as a text file.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **AI/ML**: HuggingFace Transformers, NLTK, Rake-NLTK
- **Frontend**: HTML5, Vanilla CSS, JavaScript

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd AI-text-summarizer
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python -m app.main
```
The app will be available at `http://localhost:8000`.

## 📝 Sample Input for Testing
> "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Beyond the technical aspects, AI also raises important ethical questions regarding privacy, automation of jobs, and the potential for bias in algorithmic decision-making. As the technology continues to evolve rapidly, society must adapt to its integration into daily life, from healthcare diagnostics to autonomous transportation and personalized entertainment."

## 📄 License
MIT License
