from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

import lib.response.response as response
from application import jwt
from lib.error_handlers.constants import *
from lib.response.constants import *


def server_error_response(error):
    current_app.log_exception(error)
    return response.error(status_code=500, message=MESSAGE_500)


@current_app.errorhandler(404)
def error_handler_404(error):
    return response.error(status_code=404, message=MESSAGE_404)


@current_app.errorhandler(500)
def error_handler_500(error):
    return server_error_response(error)


@current_app.errorhandler(SQLAlchemyError)
def error_handler_SQL(error):
    return server_error_response(error)


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, _jwt_data):
    return response.error(status_code=UNAUTHORIZED_ACCESS, message=TOKEN_EXPIRED)


@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return response.error(status_code=UNPROCESSABLE_ENTITY, message=error_string)


@jwt.unauthorized_loader
def unauthorized_callback(error_string):
    return response.error(status_code=UNAUTHORIZED_ACCESS, message=error_string)


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(_jwt_header, _jwt_data):
    return response.error(status_code=UNAUTHORIZED_ACCESS, message=FRESH_TOKEN_REQUIRED)


@jwt.revoked_token_loader
def revoked_token_callback(_jwt_header, _jwt_data):
    return response.error(status_code=UNAUTHORIZED_ACCESS, message=TOKEN_REVOKED)


@jwt.user_lookup_error_loader
def user_lookup_error_callback(jwt_header, jwt_data):
    return response.error(status_code=UNAUTHORIZED_ACCESS, message=ERROR_LOADING_USER)


@jwt.token_verification_failed_loader
def token_verification_failed_callback(jwt_header, jwt_data):
    return response.error(status_code=BAD_REQUEST, message=CLAIM_VERIFICATION_FAILED)
