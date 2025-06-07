from flask_mail import Mail, Message
from flask import Flask
from itsdangerous import URLSafeTimedSerializer

# Hardcoded configuration
SECRET_KEY = "a3c4b8f7e9d2a10d8b4f4e5c6b7d1c2a7f9e3b6a4d8c5e7f9a3d4b6e8c7a2d1"
MAIL_USERNAME = "thavamkajan0901@gmail.com"  # Replace with your email
MAIL_PASSWORD = "fmnp ktwg okjk dvoy"  # Replace with your email password


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
        verification_url = f"http://13.247.207.132:5000/auth/verify/{token}"  # Replace with your domain or IP

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

def send_merch_order_email(data, status):
    """
    Sends a merchandise order confirmation email to the customer.

    :param data: Dictionary containing product and customer details.
    :param order_id: Unique ID of the order.
    :param status: Current status of the order (e.g., 'confirmed', 'shipped', etc.).
    """
    try:
        msg = Message(
            subject=f"Your Merchandise Order with Club #{data['club_id']}",
            sender=MAIL_USERNAME,
            recipients=[data['customer_email']],
            body=(
                f"Hi {data['customer_name']},\n\n"
                f"Thank you for ordering with Club #{data['club_id']}!\n\n"
                f"We’re excited to let you know that your merchandise order has been received and is currently {status}.\n"
                f"Below are the details of your order:\n\n"
                f"Product: {data['product_name']}\n"
                f"Number of Items: {data['product_quantity']}\n"
                f"Total Amount Paid: ₹{data['order_amount']}\n\n"
                f"Our team is now processing your order, and you will receive updates at every important step—"
                f"whether it's being packed, shipped, or ready for pickup/delivery.\n\n"
                f"If you have any questions or notice something wrong with your order details, "
                f"feel free to reach out to us as soon as possible.\n\n"
                f"Thank you again for supporting the club and being an active part of our community. "
                f"We hope you love your merchandise!\n\n"
                f"Warm regards,\n"
                f"Club #{data['club_id']} Management Team"
            )
        )

        with service_app.app_context():
            mail.send(msg)
        print(f"Merchandise order email sent to {data['customer_email']}.")

    except Exception as e:
        print(f"Error sending merchandise order email: {e}")

def send_task_assignment_email(assignee_email, member_name, data):
    """
    Sends an email to notify a member about a new task assignment.
    """
    try:
        print(assignee_email)
        print(member_name)
        print(data)
        msg = Message(
            subject=f"New Task Assigned from Club #{data['club_id']}",
            sender=MAIL_USERNAME,
            recipients=[assignee_email],
            body=(
                f"Hi {member_name},\n\n"
                f"You’ve been assigned a new task by the admin of Club #{data['club_id']}.\n\n"
                f"Here are the details:\n\n"
                f"Task: {data['title']}\n"
                f"Description: {data['description']}\n"
                f"Priority: {data['priority']}\n"
                f"Due Date: {data['due_date']}\n\n"
                f"Please make sure to review the task and plan your time accordingly. "
                f"If you have any questions or need clarification, feel free to reach out to the club admin.\n\n"
                f"Thank you for your continued contribution to the club’s activities!\n\n"
                f"Best regards,\n"
                f"Club #{data['club_id']} Management Team"
            )
        )
        with service_app.app_context():
            mail.send(msg)
        print(f"Task assignment email sent to {assignee_email}.")

    except Exception as e:
        # You can also log this or return the error
        print(f"Error sending task assignment email: {e}")
