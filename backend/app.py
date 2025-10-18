from flask import Flask
from flask_cors import CORS
from backend.config.env_config import Config
from backend.routes.auth_routes import auth_bp
from backend.routes.document_routes import document_bp
from backend.routes.quiz_routes import quiz_bp
from backend.routes.user_routes import user_bp
from backend.routes.summary_routes import summary_bp
from backend.routes.chat_routes import chat_bp

app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(document_bp, url_prefix="/api/documents")
app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(summary_bp, url_prefix="/api/summary")
app.register_blueprint(chat_bp, url_prefix="/api/chat")

@app.route("/")
def home():
    return {"message": "Study Buddy API is running!"}

@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint not found"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    app.run(debug=Config.FLASK_DEBUG, port=5050)
