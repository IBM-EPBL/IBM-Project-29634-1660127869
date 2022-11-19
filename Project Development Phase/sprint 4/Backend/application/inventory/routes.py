from flask import Blueprint

from application.inventory.controllers import (create, delete_by_id, get_all,
                                               get_by_id, update_by_id)

inventory_blueprint = Blueprint('inventory', __name__)


inventory_blueprint.add_url_rule(rule='/',
                                 view_func=create,
                                 endpoint='create',
                                 methods=['POST'])

inventory_blueprint.add_url_rule(rule='/all',
                                 view_func=get_all,
                                 endpoint='get_all',
                                 methods=['GET'])

inventory_blueprint.add_url_rule(rule='/<int:id>',
                                 view_func=get_by_id,
                                 endpoint='get_by_id',
                                 methods=['GET'])

inventory_blueprint.add_url_rule(rule='/<int:id>',
                                 view_func=update_by_id,
                                 endpoint='update_by_id',
                                 methods=['PUT'])

inventory_blueprint.add_url_rule(rule='/<int:id>',
                                 view_func=delete_by_id,
                                 endpoint='delete_by_id',
                                 methods=['DELETE'])
