#!/usr/bin/env python3
"""
This class manages the API
authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class manages the API authentication
    """
    def __init__(self):
        """Initialization method"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Requesting authentication from the client"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Strip trailing slash from both path and excluded path
        strip_path = path.rstrip('/')
        strip_excluded_path = [p.rstrip('/') for p in excluded_paths]

        if strip_path in strip_excluded_path:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorizing the HTTP request header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
