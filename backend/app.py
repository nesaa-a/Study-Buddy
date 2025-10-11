from flask import Flask
from flask_cors import CORS
from backend.routes.auth_routes import auth_bp
from backend.routes.document_routes import document_bp
from backend.routes.quiz_routes import quiz_bp
from backend.routes.user_routes import user_bp

app = Flask(__name__)
CORS(app)

# Regjistrimi i routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(document_bp, url_prefix="/api/documents")
app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
app.register_blueprint(user_bp, url_prefix="/api/users")

@app.route("/")
def home():
    return {"message": "Study Buddy API is running!"}

if __name__ == "__main__":
    app.run(debug=True, port=5050)
