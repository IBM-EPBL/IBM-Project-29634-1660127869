from functools import wraps

from flask_jwt_extended import current_user

from application.inventory.models import Inventory
from application.location.models import Location
from application.product.models import Product


def load_product_by_id(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        product = Product.query.filter_by(
            id=kwargs['id'], retailer_id=current_user.id).one_or_404()
        return function(product)
    return decorated_function


def load_location_by_id(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        location = Location.query.filter_by(
            id=kwargs['id'], retailer_id=current_user.id).one_or_404()
        return function(location)
    return decorated_function


def load_inventory_item_by_id(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        inventory = Inventory.query \
            .filter_by(id=kwargs['id']) \
            .where(Inventory.product_id
                   .in_(Product.query
                        .with_entities(Product.id).filter_by(retailer_id=current_user.id))) \
            .one_or_404()
        return function(inventory)
    return decorated_function
