#!/usr/bin/env python3
"""
Session Authentication class that inherits
from the Auth class
"""

import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Managing sessions for authenticated users
    """
    user_id_by_session_id = {}

    def __init__(self):
        """
        Initialization method
        """
        pass

    def create_session(self, user_id: str = None) -> str:
        """Creating a session for an authenticated
        user with a user_id
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returning a User ID based on the session ID"""

        if session_id is None:
            return None

        if not isinstance(session_id, str):
            return None

        # Getting the user_id from the dictionary
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """Using a session ID to identify a user"""
        # Fetching the cookie value from the request header
        session_id = self.session_cookie(request)
        # Retrieving the user_id based on the cookie value
        user_id = self.user_id_for_session_id(session_id)

        # Fetching the user from the database
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """Deleting a session for an authenticated
        user session
        """
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
