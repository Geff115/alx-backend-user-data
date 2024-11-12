#!/usr/bin/env python3
"""
A class that inherits from Auth
"""

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Returning the decoded value of a base64 string in
        the authorization header
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """This method returns the user's email and password from the
        Base64 decoded string
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        # getting the email and password by slicing the string
        string_header = decoded_base64_authorization_header
        for i in range(len(string_header)):
            if string_header[i] == ":":
                email = string_header[:i]
                password = string_header[i+1:]
                return email, password

        return None, None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """This method returns the User instance based on
        his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # fetching the user from the database based on user_email
        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
