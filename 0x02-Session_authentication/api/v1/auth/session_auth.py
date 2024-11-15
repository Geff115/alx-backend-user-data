#!/usr/bin/env python3
"""
Session Authentication class that inherits
from the Auth class
"""

import uuid
import os
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

    def destroy_session(self, request=None):
        """Deleting the user session/logout"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
