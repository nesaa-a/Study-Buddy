from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber

app = FastAPI()

# 🚀 Lejo CORS që frontend-i të ketë qasje
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # mund të kufizohet vetëm për http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return {"filename": file.filename, "content": text}
    except Exception as e:
        return {"error": str(e)}
    

    # Leximi i tekstit nga PDF
    text = ""
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

    return {
        "filename": file.filename,
        "status": "saved",
        "extracted_text": text[:500]  # vetëm 500 karaktere për test
    }
