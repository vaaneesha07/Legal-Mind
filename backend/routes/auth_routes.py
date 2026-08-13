from flask import Blueprint, request
from services.register import register_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    return register_user(request.form, request.files)