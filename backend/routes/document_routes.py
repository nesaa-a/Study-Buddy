from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os

from backend.models.document_model import save_document, get_user_documents
from backend.utils.jwt_utils import verify_token

# Initialize Blueprint
document_bp = Blueprint("document_bp", __name__)

# Folder for uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    # Save document in DB (linked to authenticated user)
    save_document(request.user_id, filename, file_path)

    return jsonify({"message": "File uploaded successfully!", "file": filename})


# 📄 Get all documents for authenticated user
@document_bp.route("/my-documents", methods=["GET"])
@verify_token()
def get_my_documents():
    """Get user's documents - requires authentication"""
    docs = get_user_documents(request.user_id)
    return jsonify({"documents": docs})


# 📁 Serve uploaded files
@document_bp.route("/uploads/<filename>", methods=["GET"])
def serve_uploaded_file(filename):
    """Serve uploaded documents"""
    return send_from_directory(UPLOAD_FOLDER, filename)
