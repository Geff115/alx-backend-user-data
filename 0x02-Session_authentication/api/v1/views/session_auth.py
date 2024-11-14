#!/usr/bin/env python3
"""
Session Authentication view
"""

import os
from flask import jsonify, request, Response
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> Response:
    """Authenticating a user session"""
    # Getting the email and password parameters
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if not password or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    # Searching the User database with the email to retrieve a user
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    # Creating a session for the user
    session_id = auth.create_session(user.id)

    # Return user info and set session cookie
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
