from flask import Blueprint
from application.auth.controllers import register, login


auth_blueprint = Blueprint('auth', __name__)


auth_blueprint.add_url_rule(rule='/register',
                            view_func=register,
                            endpoint='register',
                            methods=['POST'])

auth_blueprint.add_url_rule(rule='/login',
                            view_func=login,
                            endpoint='login',
                            methods=['POST'])
