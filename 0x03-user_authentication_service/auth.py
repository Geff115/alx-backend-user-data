#!/usr/bin/env python3
"""
Defining a hash password method
that returns bytes
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """A method that register users based on their
        email and hashes their password
        """
        if not isinstance(email, str) or not isinstance(password, str):
            raise ValueError("Email and Password must be a string")

        # Checking if a user already exist
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hashing the password if user does not exist
        hashed_password = _hash_password(password)
        # Adding the user to the database
        user = self._db.add_user(email=email, hashed_password=hashed_password)

        return user


def _hash_password(password: str) -> bytes:
    """Hashing password with bcrypt
    and returning it in bytes
    """
    if not password or not isinstance(password, str):
        raise ValueError("Password must be provided and it must be a string")

    # Coverting password into bytes
    bytes_password = password.encode("utf-8")
    # Generating salt for bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)

    return hashed_password
