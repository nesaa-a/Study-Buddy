from flask import Blueprint, request, jsonify
from backend.utils.jwt_utils import verify_token
from backend.models.document_model import get_document_by_id
from backend.services.file_reader import read_text_from_file
from backend.services.langchain_ai import chat_with_context
from backend.services.semantic_memory import retrieve_context

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
        # fetch only if authorized
        doc = get_document_by_id(document_id, request.user_id)
        if doc:
            context_text = read_text_from_file(doc.get('file_path'))

    # Retrieve semantic memory context (top-k chunks) using user's index
    try:
        topk_contexts = retrieve_context(request.user_id, message, k=3)
        if topk_contexts:
            extra = "\n\n".join(topk_contexts)
            context_text = (context_text + "\n\n" + extra) if context_text else extra
    except Exception:
        pass

    # Generate LLM-based reply (falls back gracefully if no API key)
    reply = chat_with_context(message, context_text)

    return jsonify({
        "message": reply,
        "echo": message,
        "document_id": document_id,
        "has_context": bool(context_text)
    }), 200


