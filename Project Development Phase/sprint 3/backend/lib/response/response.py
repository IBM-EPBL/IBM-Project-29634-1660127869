from flask import jsonify

from lib.response.constants import ERROR, SUCCESS


def response(status_code, status, data, message):
    response_data = {
        'status_code': status_code,
        'status': status,
        'data': data,
        'message': message
    }
    return jsonify(response_data), status_code


def success(status_code=200, data={}, message=SUCCESS):
    return response(status_code, SUCCESS, data, message)


def error(status_code=500, data={}, message=ERROR):
    return response(status_code, ERROR, data, message)
