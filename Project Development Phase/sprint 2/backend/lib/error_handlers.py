from flask import current_app

from lib.response import response


@current_app.errorhandler(404)
def error_handler_404(_error):
    return response(status_code=404, status='error', data={}, message='Requested resource/page Found.')
