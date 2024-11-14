#!/usr/bin/env python3
"""
Session Authentication class that inherits
from the Auth class
"""

import uuid
import os
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from models.user import User
from flask import jsonify, request, Response


class SessionAuth(Auth):
    """Managing sessions for authenticated users
    """
    user_id_by_session_id = {}

    def __init__(self):
        """Initialization method"""
        pass

    def create_session(self, user_id: str = None) -> str:
        """Creating a session ID for an authenticated
        user ID
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        # Setting the key of the dictionary user_id_by_session_id
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returning a user ID based on a Session ID"""
        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        if request is None:
            return None

        # Getting the session id from the request header
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        # Getting user id from the dictionary via the session_id as key
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        # Retrieving the user from the database based on user id
        user = User.get(user_id)
        return user


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
