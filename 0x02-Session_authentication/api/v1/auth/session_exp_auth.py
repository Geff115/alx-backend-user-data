#!/usr/bin/env python3
"""
Expiration for a session
"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Expiration"""

    def __init__(self):
        """Initialization method"""
        self.session_duration = int(os.getenv('SESSION_DURATION'), 0)

    def create_session(self, user_id=None):
        """Create session for user"""
        if not user_id:
            return None

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Store a session id with user id and created_at
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id for a session if it
        is still valid.
        """
        if not session_id:
            return None

        # Getting session data
        session_data = self.user_id_by_session_id.get(session_id)
        if not session_data:
            return None

        user_id = session_data.get('user_id')
        created_at = session_data.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        if datetime.now() > created_at + \
           timedelta(seconds=self.session_duration):
            return None

        return user_id
