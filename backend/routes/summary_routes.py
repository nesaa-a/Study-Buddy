from flask import Blueprint, request, jsonify
from backend.models.summary_model import save_summary
from backend.utils.jwt_utils import verify_token
import random
import traceback

summary_bp = Blueprint("summary_bp", __name__)

@summary_bp.route("/generate", methods=["POST"])
#@verify_token()
def generate_summary():
    try:
        data = request.get_json(force=True)
        document_id = data.get("document_id")
        length = data.get("length", "medium")

        if not document_id:
            return jsonify({"error": "Missing document_id"}), 400

        # Fake AI summary (for testing)
        fake_summary = (
            f"This is a {length} AI-generated summary for document ID {document_id}. "
            f"It summarizes key points and ideas using a simulated AI model. "
            f"(random ID: {random.randint(1000, 9999)})"
        )

        # Save in DB
        save_summary(document_id, fake_summary)

        print("✅ Summary generated:", fake_summary)  # DEBUG log
        return jsonify({"success": True, "summary": fake_summary}), 200

    except Exception as e:
        print("❌ Error in generate_summary:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
