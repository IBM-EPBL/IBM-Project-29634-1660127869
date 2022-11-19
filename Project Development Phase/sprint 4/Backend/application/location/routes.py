from flask import Blueprint

from application.location.controllers import *

locations_blueprint = Blueprint('locations', __name__)


locations_blueprint.add_url_rule(rule='/',
                                 view_func=create,
                                 endpoint='create',
                                 methods=['POST'])

locations_blueprint.add_url_rule(rule='/all',
                                 view_func=get_all,
                                 endpoint='get_all',
                                 methods=['GET'])

locations_blueprint.add_url_rule(rule='/<int:id>',
                                 view_func=get_by_id,
                                 endpoint='get_by_id',
                                 methods=['GET'])

locations_blueprint.add_url_rule(rule='/<int:id>',
                                 view_func=update_by_id,
                                 endpoint='update_by_id',
                                 methods=['PUT'])

locations_blueprint.add_url_rule(rule='/<int:id>',
                                 view_func=delete_by_id,
                                 endpoint='delete_by_id',
                                 methods=['DELETE'])
