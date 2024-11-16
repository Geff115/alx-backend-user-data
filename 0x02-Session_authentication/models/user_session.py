#!/usr/bin/env python3
"""A database model that inherits from Base
"""

from models.base import Base


class UserSession(Base):
    """Managing Users session in
    the database securely
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Session instance"""
        super().__init__(*args, **kwargs)
        self.user_id = str(kwargs.get('user_id'))
        self.session_id = str(kwargs.get('session_id'))
