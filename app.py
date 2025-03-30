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
from service.chatbot import chat
from openai import AzureOpenAI
app = Flask(__name__)
# Enable CORS globally for all routes
CORS(app, supports_credentials=True)
# Register Blueprints
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(club_bp, url_prefix='/club')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(membership_bp, url_prefix='/membership')
app.register_blueprint(notification_admin_bp, url_prefix='/notification_admin')
app.register_blueprint(event_bp, url_prefix='/event')

# Azure OpenAI credentials
AZURE_API_KEY = "0b9c53361dc945f4a866356180073582"
AZURE_ENDPOINT = "https://iwmi-chat-demo.openai.azure.com/"
AZURE_API_VERSION = "2024-02-15-preview"
AZURE_DEPLOYMENT_NAME = "iwmi-gpt-4o"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=AZURE_API_VERSION,
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
)

def generate_response(question, history, max_tokens=1024, temperature=0.7, top_p=0.95):
    """
    Generate response from Azure OpenAI GPT-4o with streaming.
    """
    system_message = (
        """You are a helpful assistant. Your name is NexusAssistant.the currently we focous on university of kelaniya , below the details about club details\n
SESA Club
The Software Engineering Students' Association (SESA) is the official student society for Software Engineering undergraduates at the Faculty of Science, University of Kelaniya. It aims to foster both technical and soft skill development among students, promote collaboration, and unite undergraduates through a variety of educational and community-focused initiatives. SESA serves as a platform for members to network, share knowledge, and develop essential professional competencies.
SESA organizes key events such as RealHack, a hackathon designed to encourage innovation and problem-solving, and Junior Hack, aimed at nurturing the coding skills of junior students. Inceptio celebrates the achievements of final-year undergraduates as they transition to the professional world. Other notable initiatives include Node Fall, an entertainment event for social interaction, and beach cleaning programs promoting environmental responsibility. Additionally, the club conducts outbound training programs to develop leadership and teamwork among students.
\n
Gavel Club
The Gavel Club at the University of Kelaniya, established on October 21, 2004, is the first Gavel Club in South Asia and operates under the patronage of the Career Guidance Unit. Affiliated with Toastmasters International USA, it provides a supportive platform for undergraduates to enhance their public speaking, English language, and leadership skills. The club's vision is to empower members to be recognized as effective communicators with strong personalities, fostering self-confidence and personal growth.
The club hosts weekly educational meetings where members engage in speaking exercises and receive constructive feedback. Flagship events include the Best Speaker Contest, an inter-university public speaking competition, and the Inter-School Best Speaker Contest, aimed at nurturing young speakers. The Gavel Club also promotes collaboration through joint meetings with other university Gavel Clubs and themed sessions. These initiatives contribute to the development of communication and leadership skills in a dynamic and inclusive environment.
 """
    )

    messages = [{"role": "system", "content": system_message}]

    for msg in history:
        role = "user" if msg["sender"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["text"]})

    messages.append({"role": "user", "content": f"Question: {question}"})

    try:
        # Stream response from Azure OpenAI
        def stream():
            response = client.chat.completions.create(
                model=AZURE_DEPLOYMENT_NAME,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=True,  # Enable streaming
            )
            for chunk in response:
                if chunk.choices:
                    yield chunk.choices[0].delta.content or ""

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
        data = request.get_json()
        question = data.get("question", "")
        history = data.get("history", [])

        response_stream = generate_response(question, history)

        def stream_response():
            yield '{"text": "'
            for token in response_stream:
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
