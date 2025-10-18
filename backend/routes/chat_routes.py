from flask import Blueprint, request, jsonify
from backend.utils.jwt_utils import verify_token
from backend.models.document_model import get_document_by_id
from backend.services.file_reader import read_text_from_file

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/message', methods=['POST'])
@verify_token()
def chat_message():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    document_id = data.get('document_id')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    context_text = None
    if document_id:
        doc = get_document_by_id(document_id)
        if doc:
            context_text = read_text_from_file(doc.get('file_path'))

    # Minimal heuristic response using context availability
    if context_text:
        reply = (
            "I reviewed your document and here is a brief tip based on it: "
            "Focus on the main topics and definitions early in the text. "
            "Ask a specific question about a section or concept for a deeper answer."
        )
    else:
        reply = (
            "I couldn't access the document content right now, but I'm here to help. "
            "Please ask a specific question and, if possible, try again with a selected document."
        )

    return jsonify({
        "message": reply,
        "echo": message,
        "document_id": document_id,
        "has_context": bool(context_text)
    }), 200


