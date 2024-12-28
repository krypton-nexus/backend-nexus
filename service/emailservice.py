from flask_mail import Mail, Message
from flask import Flask
from itsdangerous import URLSafeTimedSerializer

# Hardcoded configuration
SECRET_KEY = "a3c4b8f7e9d2a10d8b4f4e5c6b7d1c2a7f9e3b6a4d8c5e7f9a3d4b6e8c7a2d1"
MAIL_USERNAME = "uok.nexus@gmail.com"  # Replace with your email
MAIL_PASSWORD = "mfaq dcij bdgc lgwj"  # Replace with your email password


# Create a local Flask app instance for email service
service_app = Flask(__name__)
service_app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
)

# Initialize Flask-Mail
mail = Mail(service_app)

# Serializer for generating secure tokens
serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_verification_token(email):
    """
    Generates a time-limited token for email verification.
    :param email: User's email address.
    :return: A secure token as a string.
    """
    return serializer.dumps(email, salt="email-verification-salt")

def send_verification_email(email, name):
    """
    Sends a verification email to the user with a clickable link.
    :param email: Recipient's email address.
    :param name: Recipient's name.
    """
    try:
        # Generate the verification token
        token = generate_verification_token(email)
        verification_url = f"http://43.205.202.255:5000/auth/verify/{token}"  # Replace with your domain or IP

        msg = Message(
            subject="Verify Your Email",
            sender=MAIL_USERNAME,
            recipients=[email],
            body=(
                f"Hi {name},\n\n"
                f"Welcome to our platform! Please verify your email by clicking the link below:\n\n"
                f"{verification_url}\n\n"
                f"If you did not sign up, please ignore this email.\n\n"
                f"Thanks!"
            )
        )

        # Use the local service app's app context to send the email
        with service_app.app_context():
            mail.send(msg)
        print(f"Verification email sent to {email}.")
    except Exception as e:
        print(f"Error sending email: {e}")


def send_admin_notification(email, member_name, club_id):
    """
    Sends an email notification to the admin when a student requests membership to a club.
    :param email: Admin's email address.
    :param member_name: Name of the student requesting membership.
    :param club_id: Club ID for which the membership is requested.
    """
    try:
        msg = Message(
            subject="New Membership Request",
            sender=MAIL_USERNAME,
            recipients=[email],
            body=(
                f"Hi Admin,\n\n"
                f"A new membership request has been made by {member_name} for Club ID: {club_id}.\n\n"
                f"Please log in to the dashboard to take appropriate action.\n\n"
                f"Thank you!"
            )
        )

        # Use the local service app's app context to send the email
        with service_app.app_context():
            mail.send(msg)
        print(f"Notification email sent to admin: {email}.")
    except Exception as e:
        print(f"Error sending email to admin: {e}")
