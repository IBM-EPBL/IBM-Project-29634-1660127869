from flask import jsonify


class Response():
    @staticmethod
    def success(data):
        response = {
            'status': 'success',
            'data': data
        }
        return jsonify(response), 200

    @staticmethod
    def error(data, error_code):
        response = {
            'status': 'error',
            'code': error_code,
            'data': data
        }
        return jsonify(response), error_code
