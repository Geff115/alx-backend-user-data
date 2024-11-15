#!/usr/bin/env python3
"""
Session Authentication class that inherits
from the Auth class
"""

import uuid
import os
from api.v1.auth.auth import Auth
from models.user import User
from flask import jsonify, request, Response


class SessionAuth(Auth):
    """Managing sessions for authenticated users
    """
    #user_id_by_session_id = {}
