import re
import os
import uuid
import smtplib
from email.mime.text import MIMEText
from database.connections import users_collection, documents_collection
from flask import jsonify

# Folder where uploaded documents get saved on disk.
# Created automatically if it doesn't exist yet.
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads", "user_documents")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(file_storage, user_email):
    """
    Saves an uploaded file (e.g. request.files['document']) to disk
    with a unique filename, and returns the path it was saved to.
    """
    _, ext = os.path.splitext(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_FOLDER, unique_name)

    file_storage.save(save_path)
    return save_path

# --- Email configuration ---
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_app_password"
SENDER_EMAIL = "your_email@gmail.com"
SENDER_NAME = "Legal Mind"


def send_confirmation_email(to_email, username):
    subject = "Welcome to Legal Mind — Registration Successful"
    body = (
        f"Hi {username},\n\n"
        "Your account with Legal Mind has been successfully created.\n"
        "You can now log in and start using the platform.\n\n"
        "If you did not create this account, please contact our support team.\n\n"
        "— The Legal Mind Team"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"[email] Failed to send confirmation email to {to_email}: {e}")
        return False


def register_user(data, files=None):
    files = files or {}
    data = dict(data)  # request.form is immutable; convert to a regular dict we can work with

    required_fields = ["name", "email", "password", "phone", "role"]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"success": False, "message": f"{field} is required"}), 400

    role = data["role"].strip().lower()

    valid_roles = ["public", "student", "lawyer"]
    if role not in valid_roles:
        return jsonify({"success": False, "message": "Invalid role"}), 400

    if role == "lawyer" and "document" not in files:
        return jsonify({"success": False, "message": "Bar Council ID / License document is required for lawyers"}), 400

    if role == "student" and "idProof" not in files:
        return jsonify({"success": False, "message": "ID proof is required for students"}), 400

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, data["email"]):
        return jsonify({"success": False, "message": "Invalid email address"}), 400

    phone_pattern = r"^[0-9]{10}$"
    if not re.match(phone_pattern, data["phone"]):
        return jsonify({"success": False, "message": "Invalid phone number, must be 10 digits"}), 400

    password = data["password"]

    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must contain at least 8 characters"}), 400
    if not re.search(r"[A-Z]", password):
        return jsonify({"success": False, "message": "Password must contain at least one uppercase letter"}), 400
    if not re.search(r"[a-z]", password):
        return jsonify({"success": False, "message": "Password must contain at least one lowercase letter"}), 400
    if not re.search(r"[0-9]", password):
        return jsonify({"success": False, "message": "Password must contain at least one number"}), 400
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return jsonify({"success": False, "message": "Password must contain at least one special character"}), 400

    existing_user = users_collection.find_one({
        "$or": [{"email": data["email"]}, {"phone": data["phone"]}]
    })

    if existing_user:
        return jsonify({"success": False, "message": "User already exists"}), 409

    result = users_collection.insert_one(data)
    new_user_id = str(result.inserted_id)

    if role == "lawyer" and "document" in files:
        saved_path = save_uploaded_file(files["document"], data["email"])
        documents_collection.insert_one({
            "userId": new_user_id,
            "type": "bar_council_document",
            "filePath": saved_path,
            "originalFilename": files["document"].filename
        })

    if role == "student" and "idProof" in files:
        saved_path = save_uploaded_file(files["idProof"], data["email"])
        documents_collection.insert_one({
            "userId": new_user_id,
            "type": "id_proof",
            "filePath": saved_path,
            "originalFilename": files["idProof"].filename
        })

    send_confirmation_email(data["email"], data["name"])

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user": {
            "userId": new_user_id,
            "name": data["name"],
            "email": data["email"],
            "role": role
        }
    }), 201


def login_user(data):
    if "email" not in data or "password" not in data:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, data["email"]):
        return jsonify({"success": False, "message": "Invalid email format"}), 400

    user = users_collection.find_one({"email": data["email"], "password": data["password"]})

    if user:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "userId": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200

    return jsonify({"success": False, "message": "Invalid email or password"}), 401