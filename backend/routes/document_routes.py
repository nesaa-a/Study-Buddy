from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from backend.models.document_model import save_document, get_user_documents
from backend.utils.jwt_utils import verify_token

document_bp = Blueprint("document_bp", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload file
@document_bp.route("/upload", methods=["POST"])
@verify_token
def upload_file():
    user_id = request.form.get("user_id")
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    save_document(user_id, filename, file_path)
    
    return jsonify({"message": "File uploaded successfully!", "file": filename})

# Get all documents for a user
@document_bp.route("/user/<int:user_id>/documents", methods=["GET"])
def get_documents(user_id):
    docs = get_user_documents(user_id)
    return jsonify(docs)
