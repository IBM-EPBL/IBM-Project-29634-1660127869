from flask import Blueprint

from application.marketplace.controllers import (
    complete_purchase_order, get_all_locations_for_a_retailer,
    get_all_products_for_a_location, get_all_retailers)

marketplace_blueprint = Blueprint('marketplace', __name__)


marketplace_blueprint.add_url_rule(rule='/retailers',
                                   view_func=get_all_retailers,
                                   endpoint='get_all_retailers',
                                   methods=['GET'])

marketplace_blueprint.add_url_rule(rule='/locations/<int:retailer_id>',
                                   view_func=get_all_locations_for_a_retailer,
                                   endpoint='get_all_locations_for_a_retailer',
                                   methods=['GET'])

marketplace_blueprint.add_url_rule(rule='/products/<int:location_id>',
                                   view_func=get_all_products_for_a_location,
                                   endpoint='get_all_products_for_a_location',
                                   methods=['GET'])

marketplace_blueprint.add_url_rule(rule='/order',
                                   view_func=complete_purchase_order,
                                   endpoint='complete_purchase_order',
                                   methods=['POST'])
