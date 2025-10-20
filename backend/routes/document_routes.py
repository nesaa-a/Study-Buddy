from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

from backend.models.document_model import save_document, get_user_documents, get_document_by_id
from backend.services.semantic_memory import build_or_update_user_index
from backend.utils.jwt_utils import verify_token

# External libraries for reading files
from PyPDF2 import PdfReader
import docx2txt
import pdfplumber

# Initialize Blueprint
document_bp = Blueprint("document_bp", __name__)

# Folder for uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🧩 Helper function: Extract text content from different file types
def extract_text_from_file(file_path):
    text = ""
    try:
        if file_path.endswith(".pdf"):
            # First try PyPDF2
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += (page.extract_text() or "")
            # If PyPDF2 yields too little text, fallback to pdfplumber for better quality
            if len((text or '').strip()) < 400:
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text = " ".join([p.extract_text() or "" for p in pdf.pages])
                except Exception as _:
                    pass
        elif file_path.endswith(".docx"):
            text = docx2txt.process(file_path)
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    except Exception as e:
        print(f"⚠️ Error extracting text: {e}")
    return text.strip()


# 📤 Upload file
@document_bp.route("/upload", methods=["POST"])
@verify_token()
def upload_file():
    """Upload document - requires authentication"""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # ✅ Extract text content from the uploaded file
    text_content = extract_text_from_file(file_path)

    # ✅ Save document in DB (linked to authenticated user)
    save_document(request.user_id, filename, file_path, text_content)

    # 🔎 Update semantic index for this user (best-effort)
    try:
        def _fetch(doc_id, user_id):
            return get_document_by_id(doc_id, user_id)
        build_or_update_user_index(request.user_id, _fetch)
    except Exception as _:
        pass

    return jsonify({"message": "File uploaded successfully!", "file": filename})


# 📄 Get all documents for authenticated user
@document_bp.route("/my-documents", methods=["GET"])
@verify_token()
def get_my_documents():
    """Get user's documents - requires authentication"""
    docs = get_user_documents(request.user_id)
    return jsonify({"documents": docs})


# 🧾 Get a single document including text content
@document_bp.route("/<int:document_id>", methods=["GET"])
@verify_token()
def get_single_document(document_id):
    """Fetch a specific document's metadata and text content"""
    doc = get_document_by_id(document_id, request.user_id)
    if not doc:
        return jsonify({"error": "Document not found"}), 404

    return jsonify({
        "id": doc["id"],
        "filename": doc["filename"],
        "content": doc["content"],
    })


# 📁 Serve uploaded files
@document_bp.route("/uploads/<filename>", methods=["GET"])
def serve_uploaded_file(filename):
    """Serve uploaded documents"""
    return send_from_directory(UPLOAD_FOLDER, filename)
