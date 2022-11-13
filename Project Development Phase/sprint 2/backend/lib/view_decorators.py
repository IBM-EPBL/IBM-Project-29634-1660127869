from functools import wraps

from flask_jwt_extended import current_user

from application.product.models import Product


def load_product_by_id(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        product = Product.query.filter_by(
            id=kwargs['id'], retailer_id=current_user.id).one_or_404()
        return function(product)
    return decorated_function
