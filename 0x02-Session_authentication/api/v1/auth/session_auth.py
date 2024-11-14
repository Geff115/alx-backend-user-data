#!/usr/bin/env python3
"""
Session Authentication class that inherits
from the Auth class
"""

import uuid
from api.v1.auth.auth import Auth


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
