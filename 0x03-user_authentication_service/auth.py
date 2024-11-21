#!/usr/bin/env python3
"""
Defining a hash password method
that returns bytes
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validating a user's login credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Creating a session for the user and
        returning the session id as a string
        """
        # Finding the user corresponding to the email
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        user.session_id = session_id
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Geetting a user based on session id"""
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """This method updates the corresponding user's
        session id to None
        """
        if not user_id:
            return None

        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user_id, session_id=None)


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


def _generate_uuid() -> str:
    """Generating a uuid string"""
    id_string = str(uuid.uuid4())
    return id_string
