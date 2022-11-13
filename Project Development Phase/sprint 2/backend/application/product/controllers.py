from flask_jwt_extended import current_user, jwt_required

from application import db
from application.product.constants import *
from application.product.forms import ProductEditForm, ProductForm
from application.product.models import Product
from lib.constants import *
from lib.response import response
from lib.response_status_codes import *
from lib.view_decorators import load_product_by_id


@jwt_required()
def create():
    form = ProductForm()

    if form.validate():
        product_data = {
            'name': form.name.data,
            'description': form.description.data,
            'retailer_id': current_user.id
        }
        product = Product(**product_data)

        db.session.add(product)
        db.session.commit()
        response_data = {'id': product.id}
        return response(status_code=RESOURCE_CREATED, status=SUCCESS, data=response_data, message=PRODUCT_CREATED)

    return response(status_code=UNPROCESSABLE_ENTITY, status=ERROR, data=form.errors, message=INVALID_DATA)


@jwt_required()
def get_all():
    products = [product.to_dict() for product in current_user.products]

    return response(status_code=REQUEST_COMPLETED, status=SUCCESS, data=products, message=ALL_PRODUCTS)


@jwt_required()
@load_product_by_id
def get_by_id(product):
    return response(status_code=REQUEST_COMPLETED, status=SUCCESS, data=product.to_dict(), message=PRODUCT)


@jwt_required()
@load_product_by_id
def update_by_id(product):
    form = ProductEditForm()

    if form.validate():
        form_description = form.description.data
        if form_description != product.description:
            product.description = form_description

            db.session.add(product)
            db.session.commit()
        response_data = {'description': form_description}
        return response(status_code=REQUEST_COMPLETED, status=SUCCESS, data=response_data, message=PRODUCT_UPDATED)

    return response(status_code=UNPROCESSABLE_ENTITY, status=ERROR, data=form.errors, message=INVALID_DATA)


@jwt_required()
@load_product_by_id
def delete_by_id(product):
    db.session.delete(product)
    db.session.commit()
    return response(status_code=REQUEST_COMPLETED, status=SUCCESS, data=product.to_dict(), message=PRODUCT_DELETED)
