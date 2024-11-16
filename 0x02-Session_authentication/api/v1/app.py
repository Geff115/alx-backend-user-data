#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

# Get the AUTH_TYPE environment variable
auth_type = os.getenv('AUTH_TYPE')

# Based on the value of auth_type, create instance of Auth/BasicAuth
# and SessionAuth
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
if auth_type == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
if auth_type == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """ Not allowed handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """A function that will run before each request"""
    if auth is None:
        return

    list_paths = ['/api/v1/status/',
                  '/api/v1/unauthorized/',
                  '/api/v1/forbidden/',
                  '/api/v1/auth_session/login/'
                  ]
    # Checking if request.path is not part of this list
    if request.path not in list_paths:
        if not auth.require_auth(request.path, list_paths):
            return

        if auth.authorization_header(request) is None and \
           auth.session_cookie(request) is None:
            abort(401)

        if auth.current_user(request) is None:
            abort(403)

    request.current_user = auth.current_user(request)
    # print("current_user: {}".format(request.current_user))


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
