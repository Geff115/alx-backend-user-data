#!/usr/bin/env python3
"""
A basic Flask app
"""

from flask import Flask
from flask import jsonify, request, abort, make_response
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


@app.route("/sessions", methods=["POST"])
def login():
    """The endpoint that handles user's login"""
    # fetching user's email and password from request
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password is required"}), 400

    if not AUTH.valid_login(email, password):
        abort(401)

    # Creating a session for the user
    session_id = AUTH.create_session(email)
    # setting the session_id as a cookie
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
