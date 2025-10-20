from flask import Blueprint, jsonify, request
from backend.utils.jwt_utils import verify_token
from backend.models.document_model import get_document_by_id
from backend.services.file_reader import read_text_from_file
from backend.services.langchain_ai import generate_quiz_from_text_langchain

# Krijo Blueprint për quiz routes
quiz_bp = Blueprint('quiz', __name__)

# Test route to verify authentication
@quiz_bp.route('/test', methods=['GET'])
@verify_token()
def test_quiz():
    """Test route - requires authentication"""
    return jsonify({"message": "Quiz routes working!", "user_id": request.user_id})

# Generate quiz questions
@quiz_bp.route('/generate', methods=['POST'])
@verify_token()
def generate_quiz():
    """Generate quiz from document text - requires authentication"""
    try:
        data = request.get_json() or {}

        # Accept either raw text or a document_id; prefer document_id if provided
        document_id = data.get('document_id')
        document_text = data.get('text')

        extraction_warning = None
        if document_id:
            doc = get_document_by_id(document_id, request.user_id)
            if not doc:
                return jsonify({"error": "Document not found"}), 404
            # Prefer stored DB content; fallback to reading file
            document_text = (doc.get('content') or '').strip() or document_text
            if not document_text:
                extracted = read_text_from_file(doc.get('file_path'))
                if not extracted:
                    extraction_warning = "Could not extract text from document; returning generic questions."
                    document_text = None
                else:
                    document_text = extracted

        # If there is still no text (no document_id and no text), proceed with generic questions
        if document_text:
            sample_questions = generate_quiz_from_text_langchain(document_text)
        else:
            # Generic fallback
            sample_questions = [
                {
                    "id": 1,
                    "question": "What is the main topic of the document?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 0,
                    "type": "multiple_choice"
                },
                {
                    "id": 2,
                    "question": "Summarize the key idea in one sentence.",
                    "options": [],
                    "correct_answer": None,
                    "type": "open_ended"
                }
            ]

        payload = {
            "message": "Quiz generated successfully",
            "questions": sample_questions,
            "user_id": request.user_id
        }
        if extraction_warning:
            payload["warning"] = extraction_warning
        return jsonify(payload)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to generate quiz", "details": str(e)}), 500
