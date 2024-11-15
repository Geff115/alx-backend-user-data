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
