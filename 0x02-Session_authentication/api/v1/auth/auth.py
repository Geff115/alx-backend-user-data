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

        # Strip trailing slash from path
        strip_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            # Handle wildcards
            if excluded_path.endswith('*'):
                if strip_path.startswith(excluded_path[:-1]):
                    return False
            # Handle exact matches
            elif strip_path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorizing the HTTP request header"""
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
