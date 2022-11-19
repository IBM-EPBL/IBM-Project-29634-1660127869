from flask_jwt_extended import current_user, jwt_required

import lib.response.response as response
from application import db
from application.product.constants import *
from application.product.forms import ProductEditForm, ProductForm
from application.product.models import Product
from lib.decorators import load_product_by_id
from lib.response.constants import *


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
        return response.success(status_code=RESOURCE_CREATED, data=response_data, message=PRODUCT_CREATED)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


@jwt_required()
def get_all():
    products = [product.to_dict() for product in current_user.products]

    return response.success(status_code=REQUEST_COMPLETED, data=products, message=ALL_PRODUCTS)


@jwt_required()
@load_product_by_id
def get_by_id(product):
    return response.success(status_code=REQUEST_COMPLETED, data=product.to_dict(), message=PRODUCT)


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
        return response.success(status_code=REQUEST_COMPLETED, data=response_data, message=PRODUCT_UPDATED)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


@jwt_required()
@load_product_by_id
def delete_by_id(product):
    db.session.delete(product)
    db.session.commit()
    return response.success(status_code=REQUEST_COMPLETED, data=product.to_dict(), message=PRODUCT_DELETED)
