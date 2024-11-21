#!/usr/bin/env python3
"""
A basic Flask app
"""

from flask import Flask, redirect
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


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout endpoint"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    # finding the user with the associated session_id
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        abort(403)


@app.route("/profile")
def profile():
    """Endpoint for the user's profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    # Finding the user based on the session_id retrieved
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Post reset password token"""
    email = request.form.get("email")
    if not email:
        abort(403)

    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token}), 200


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Update password endpoint"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return jsonify({"message": "Invalid reset token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
