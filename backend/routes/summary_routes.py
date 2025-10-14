from flask import Blueprint, request, jsonify
from backend.models.summary_model import save_summary
from backend.utils.jwt_utils import verify_token
import random

summary_bp = Blueprint("summary_bp", __name__)

@summary_bp.route("/generate", methods=["POST"])
@verify_token()
def generate_summary():
    data = request.get_json()
    document_id = data.get("document_id")
    length = data.get("length")

    if not document_id:
        return jsonify({"error": "Missing document_id"}), 400

    # Generate a fake summary for testing
    fake_summary = (
        f"This is a {length or 'medium'} AI-generated summary for document ID {document_id}. "
        f"It summarizes key points and ideas using a simulated AI model. "
        f"(random ID: {random.randint(1000,9999)})"
    )

    # Save to database
    save_summary(document_id, fake_summary)

    # ✅ Make sure we actually return the summary
    return jsonify({"summary": fake_summary}), 200
