import sys
import logging
from flask import request, Response,Flask,jsonify
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models'))
from huggingface_hub import InferenceClient, login
from routes.student_routes import student_bp
from routes.auth_routes import auth_bp
from routes.club_routes import club_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS
from routes.membership_routes import membership_bp
from routes.notification_admin_routes import notification_admin_bp
from routes.event_routes import event_bp
app = Flask(__name__)
CORS(app)
# Register Blueprints
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(club_bp, url_prefix='/club')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(membership_bp, url_prefix='/membership')
app.register_blueprint(notification_admin_bp, url_prefix='/notification_admin')
app.register_blueprint(event_bp, url_prefix='/event')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Hugging Face Token (Replace with your token)
HF_TOKEN = "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"
login(token=HF_TOKEN)

# Hugging Face Inference Client
client = InferenceClient("Qwen/Qwen2.5-Coder-32B-Instruct")
def generate_response(question, history, max_tokens=1024, temperature=0.7, top_p=0.95):
    """
    Generate response from Hugging Face model.
    """
    system_message = (
        "You are a helpful assistant. Your name is Kajan. The University of Kelaniya Gavel Club, affiliated to Toastmasters International USA, "
        "was chartered in October 2004 and has gained much reputation by becoming the first ever Gavel Club in South Asia. "
        "The initial step towards creating the club was taken by a Speechcrafters’ Educational Programme at the university, initiated "
        "under the guidance of Mr. Sujith Bandulahewa, the Charter President of Serendib Toastmasters Club, Prof Kapila Seneviratne "
        "and Dr. D.U. Mohan. This successful implementation favoured the goals of the educational and career aspirations and therefore "
        "gave birth to the Gavel Club of University of Kelaniya on the 21st of October 2004. The club is currently operated under the patronage "
        "of Career Guidance Unit of the University of Kelaniya."
    )

    messages = [{"role": "system", "content": system_message}]

    for msg in history:
        role = "user" if msg["sender"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["text"]})
    messages.append({"role": "system", "content": "Please answer the following question:"})
    messages.append({"role": "user", "content":f"question is :-  {question}"})

    try:
        # Streaming response from Hugging Face
        def stream():
            for chunk in client.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=True,
            ):
                yield chunk.choices[0].delta.content

        return stream()
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return f"Error: {e}"


@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint for text input.
    """
    try:
        # Parse incoming request
        data = request.get_json()

        # Extract message and history from the data
        question = data.get("question", "")
        history = data.get("history", [])
        # Generate chatbot response
        response = generate_response(question, history)

        # Format response for streaming
        def stream_response():
            yield '{"text": "'
            for token in response:
                yield token.replace('"', '\\"')  # Escape double quotes for JSON
            yield '"}'

        return Response(stream_response(), content_type="application/json")
    except Exception as e:
        logging.error(f"Error handling chat request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Nexus API"}), 200

    
@app.route('/endpoints', methods=['GET'])
def list_endpoints():
    """
    Endpoint to list all available routes in the Flask application.
    :return: JSON response containing all endpoints.
    """
    try:
        endpoints = []
        for rule in app.url_map.iter_rules():
            # Extract methods and path for each endpoint
            methods = ', '.join(rule.methods)
            endpoints.append({
                "endpoint": rule.endpoint,
                "methods": methods,
                "url": str(rule)
            })

        return jsonify({"endpoints": endpoints}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
