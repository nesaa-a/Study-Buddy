from flask import Blueprint, jsonify, request

# Krijo Blueprint për quiz routes
quiz_bp = Blueprint('quiz', __name__)

# Test route për me u siguru që funksionon
@quiz_bp.route('/test', methods=['GET'])
def test_quiz():
    return jsonify({"message": "Quiz routes working!"})


# Route për gjenerimin e pyetjeve të quizzit (placeholder)
@quiz_bp.route('/generate', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    document_text = data.get('text', '')

    # Në këtë version bazik, thjesht kthejmë disa pyetje të thjeshta testuese
    sample_questions = [
        {"question": "What is the main topic of the document?", "options": ["A", "B", "C", "D"], "answer": "A"},
        {"question": "Summarize the key idea in one sentence.", "options": [], "answer": None}
    ]

    return jsonify({
        "message": "Quiz generated successfully",
        "questions": sample_questions
    })
