from flask import Blueprint

from application.product.controllers import (create, delete_by_id, get_all,
                                             get_by_id, update_by_id)

products_blueprint = Blueprint('products', __name__)


products_blueprint.add_url_rule(rule='/',
                                view_func=create,
                                endpoint='create',
                                methods=['POST'])

products_blueprint.add_url_rule(rule='/all',
                                view_func=get_all,
                                endpoint='get_all',
                                methods=['GET'])

products_blueprint.add_url_rule(rule='/<int:id>',
                                view_func=get_by_id,
                                endpoint='get_by_id',
                                methods=['GET'])

products_blueprint.add_url_rule(rule='/<int:id>',
                                view_func=update_by_id,
                                endpoint='update_by_id',
                                methods=['PUT'])

products_blueprint.add_url_rule(rule='/<int:id>',
                                view_func=delete_by_id,
                                endpoint='delete_by_id',
                                methods=['DELETE'])
