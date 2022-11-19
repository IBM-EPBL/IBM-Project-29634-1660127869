from flask_jwt_extended import current_user, jwt_required

import lib.response.response as response
from application import db
from application.inventory.constants import *
from application.inventory.forms import InventoryEditForm, InventoryForm
from application.inventory.models import Inventory
from application.location.models import Location
from application.product.models import Product
from lib.decorators import load_inventory_item_by_id
from lib.response.constants import *


@jwt_required()
def create():
    form = InventoryForm()

    if form.validate():
        product_id = Product.query.with_entities(Product.id).filter_by(
            name=form.product_name.data, retailer_id=current_user.id).scalar()
        location_id = Location.query.with_entities(Location.id).filter_by(
            name=form.location_name.data, retailer_id=current_user.id).scalar()

        already_exists = Inventory.query.filter_by(
            product_id=product_id, location_id=location_id).scalar()

        if already_exists:
            return response.error(status_code=UNPROCESSABLE_ENTITY, message=ALREADY_EXISTS)

        inventory_data = {
            'product_id': product_id,
            'location_id': location_id,
            'quantity': form.quantity.data,
            'threshold': form.threshold.data
        }

        inventory = Inventory(**inventory_data)

        db.session.add(inventory)
        db.session.commit()
        response_data = {'id': inventory.id}
        return response.success(status_code=RESOURCE_CREATED, data=response_data, message=INVENTORY_RECORD_CREATED)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


@jwt_required()
def get_all():
    product_ids = {product.id for product in current_user.products}
    inventory_items = Inventory.query.filter(
        Inventory.product_id.in_(product_ids)).all()
    inventory_items = [inventory_item.to_dict()
                       for inventory_item in inventory_items]

    return response.success(status_code=REQUEST_COMPLETED, data=inventory_items, message=ALL_INVENTORY_ITEMS)


@jwt_required()
@load_inventory_item_by_id
def get_by_id(inventory_item):
    return response.success(status_code=REQUEST_COMPLETED, data=inventory_item.to_dict(), message=INVENTORY_ITEM)


@jwt_required()
@load_inventory_item_by_id
def update_by_id(inventory_item):
    form = InventoryEditForm()

    if form.validate():
        form_quantity = form.quantity.data
        if form_quantity != inventory_item.quantity:
            inventory_item.quantity = form_quantity

        form_threshold = form.threshold.data
        if form_threshold != inventory_item.threshold:
            inventory_item.threshold = form_threshold

        db.session.add(inventory_item)
        db.session.commit()
        response_data = {'quantity': form_quantity,
                         'threshold': form_threshold}
        return response.success(status_code=REQUEST_COMPLETED, data=response_data, message=INVENTORY_ITEM_UPDATED)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


@jwt_required()
@load_inventory_item_by_id
def delete_by_id(inventory_item):
    db.session.delete(inventory_item)
    db.session.commit()
    response_data = {'id': inventory_item.id}
    return response.success(status_code=REQUEST_COMPLETED, data=response_data, message=INVENTORY_ITEM_DELETED)
