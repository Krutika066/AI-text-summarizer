from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .summarizer import ai_summarizer
from .utils import extract_text_from_pdf, extract_text_from_txt, clean_text

app = FastAPI(title="AI Text Summarizer API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummarizeRequest(BaseModel):
    text: str
    length_type: str = "medium"

@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")
    
    cleaned_text = clean_text(request.text)
    summary, keywords = ai_summarizer.summarize(cleaned_text, request.length_type)
    
    return {
        "original_text": request.text,
        "summary": summary,
        "keywords": keywords
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), length_type: str = Form("medium")):
    content = await file.read()
    filename = file.filename.lower()
    
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif filename.endswith(".txt"):
        text = extract_text_from_txt(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or TXT.")
    
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from file.")
    
    cleaned_text = clean_text(text)
    summary, keywords = ai_summarizer.summarize(cleaned_text, length_type)
    
    return {
        "original_text": text,
        "summary": summary,
        "keywords": keywords
    }

# Mount static files (will serve the frontend from here)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
