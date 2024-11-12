#!/usr/bin/env python3
"""
A class that inherits from Auth
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic authentication header
    Inheriting from Auth
    """

    def __init__(self):
        """Initialization method"""
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracting an encoded base64 string for the
        authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]
