from flask import Blueprint, jsonify, request
from backend.utils.jwt_utils import verify_token

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
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    document_text = data.get('text', '')
    if not document_text:
        return jsonify({"error": "Document text is required"}), 400

    # Sample questions (placeholder for actual quiz generation)
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

    return jsonify({
        "message": "Quiz generated successfully",
        "questions": sample_questions,
        "user_id": request.user_id
    })
