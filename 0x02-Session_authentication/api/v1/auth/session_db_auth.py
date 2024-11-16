#!/usr/bin/env python3
"""A SessionDBAuth class that inherits from
SessionExpAuth
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """A session authenticator class for the
    session database
    """

    def create_session(self, user_id=None):
        """Creating a user session
        and storing it in the DB
        """
        if not user_id:
            return None

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        # Storing the session in UserSession
        user_session = UserSession(user_id=user_id,
                                   session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returning the user_id by querying UserSession
        with the session_id
        """
        if not session_id:
            return None

        user_id = super().user_id_for_session_id(session_id)
        return user_id

    def destroy_session(self, request=None):
        """Destroying a User's session"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
