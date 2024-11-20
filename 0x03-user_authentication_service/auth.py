#!/usr/bin/env python3
"""
Defining a hash password method
that returns bytes
"""

import bcrypt


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
