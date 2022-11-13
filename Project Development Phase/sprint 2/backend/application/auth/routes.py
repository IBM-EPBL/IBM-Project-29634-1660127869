from flask import Blueprint

from application.auth.controllers import (confirm_email, login, register,
                                          resend_confirmation_email)

auth_blueprint = Blueprint('auth', __name__)


auth_blueprint.add_url_rule(rule='/register',
                            view_func=register,
                            endpoint='register',
                            methods=['POST'])

auth_blueprint.add_url_rule(rule='/login',
                            view_func=login,
                            endpoint='login',
                            methods=['POST'])

auth_blueprint.add_url_rule(rule='/cofirm_email/<token>',
                            view_func=confirm_email,
                            endpoint='confirm_email',
                            methods=['GET'])

auth_blueprint.add_url_rule(rule='/resend_confirmation_email',
                            view_func=resend_confirmation_email,
                            endpoint='resend_confirmation_email',
                            methods=['POST'])
