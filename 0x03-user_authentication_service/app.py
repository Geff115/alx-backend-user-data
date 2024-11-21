#!/usr/bin/env python3
"""
A basic Flask app
"""

from flask import Flask
from flask import jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Root endpoint returning a welcome message in JSON format."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """The endpoint to register a user"""
    # Extracting the email and password from request
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    # Registering the user
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
