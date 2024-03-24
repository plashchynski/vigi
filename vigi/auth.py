from flask import current_app
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if not current_app.configuration_manager.http_basic_username:
        # basic auth is not configured (disabled)
        return True
    
    hashed_password = current_app.configuration_manager.http_basic_hashed_password
    if current_app.configuration_manager.http_basic_password:
        hashed_password = generate_password_hash(current_app.configuration_manager.http_basic_password)

    return username == current_app.configuration_manager.http_basic_username and check_password_hash(hashed_password, password)
