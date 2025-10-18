from flask import Blueprint, request, jsonify
from backend.models.summary_model import save_summary
from backend.services.summarizer import generate_summary
import traceback

summary_bp = Blueprint("summary_bp", __name__)

@summary_bp.route("/generate", methods=["POST"])
def summarize_document():
    try:
        data = request.get_json(force=True)
        document_id = data.get("document_id")
        text = data.get("text")
        length = data.get("length", "medium")

        if not document_id or not text:
            return jsonify({"error": "Missing document_id or text"}), 400

        summary_text = generate_summary(text, length)
        save_summary(document_id, summary_text)

        return jsonify({"success": True, "summary": summary_text}), 200

    except Exception as e:
        print("❌ Error in summarization:", e)
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
