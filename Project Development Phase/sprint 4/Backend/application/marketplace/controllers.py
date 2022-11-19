import lib.response.response as response
from application import db
from application.auth.models import Retailer
from application.inventory.models import Inventory
from application.location.models import Location
from application.marketplace.constants import *
from application.marketplace.forms import PurchaseOrderForm
from application.product.models import Product
from lib.mailer import send_restock_mail
from lib.response.constants import *


def get_all_retailers():
    retailers = [{'name': retailer.name}
                 for retailer in Retailer.query.with_entities(Retailer.name).all()]
    return response.success(status_code=REQUEST_COMPLETED, data=retailers, message=ALL_RETAILERS)


def get_all_locations_for_a_retailer(retailer_id):
    locations_for_a_retailer = Location.query.with_entities(Location.name).filter_by(
        retailer_id=retailer_id).all()
    locations_for_a_retailer = [{'name': location.name}
                                for location in locations_for_a_retailer]
    return response.success(status_code=REQUEST_COMPLETED, data=locations_for_a_retailer, message=LOCATIONS_FOR_A_RETAILER)


def get_all_products_for_a_location(location_id):
    products_for_a_location = Product.query.with_entities(Product.name).filter_by(
        retailer_id=Location.query.with_entities(Location.retailer_id).filter_by(id=location_id)).all()
    products_for_a_location = [{'name': product.name}
                               for product in products_for_a_location]
    return response.success(status_code=REQUEST_COMPLETED, data=products_for_a_location, message=PRODUCTS_FOR_A_LOCATION)


def complete_purchase_order():
    form = PurchaseOrderForm()

    if form.validate():
        form_product_name = form.product_name.data
        product_id = Product.query.with_entities(
            Product.id).filter_by(name=form_product_name).scalar()
        location_id = Location.query.with_entities(
            Location.id).filter_by(name=form.location_name.data).scalar()

        existing_product_record = Inventory.query.filter_by(
            product_id=product_id, location_id=location_id).scalar()

        if not existing_product_record:
            return response.error(status_code=UNPROCESSABLE_ENTITY, message=PRODUCT_NOT_EXIST_IN_THE_LOCATION)

        form_quantity = form.quantity.data
        if form_quantity > existing_product_record.quantity:
            return response.error(status_code=UNPROCESSABLE_ENTITY, message=TOO_MUCH_QUANTITY)

        existing_product_record.quantity -= form_quantity

        if existing_product_record.quantity <= existing_product_record.threshold:
            retailer = Retailer.query.filter_by(id=Product.query.with_entities(
                Product.retailer_id).filter_by(id=existing_product_record.product_id).scalar()).scalar()
            send_restock_mail(retailer, form_product_name)

        db.session.add(existing_product_record)
        db.session.commit()

        respose_data = {'bought': form_product_name, 'quantity': form_quantity}
        return response.success(status_code=REQUEST_COMPLETED,
                                data=respose_data, message=PURCHASE_SUCCESSFUL)

    return response.error(status_code=UNPROCESSABLE_ENTITY,
                          data=form.errors, message=INVALID_DATA)
