"""
This module provides the basic authentication for web console routes.
"""

from flask import current_app
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """
    Verify the username and password for basic authentication.
    """
    if not current_app.configuration_manager.http_basic_username:
        # basic auth is not configured (disabled)
        return True

    hashed_password = current_app.configuration_manager.http_basic_hashed_password
    http_basic_password = current_app.configuration_manager.http_basic_password
    if http_basic_password:
        # if the password is set in the configuration, generate the hash from it
        hashed_password = generate_password_hash(http_basic_password)

    if username == current_app.configuration_manager.http_basic_username and \
                check_password_hash(hashed_password, password):
        return True

    return False
