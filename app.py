import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models'))
from flask import Flask,jsonify
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
