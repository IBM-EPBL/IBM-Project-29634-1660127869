from flask_jwt_extended import current_user, jwt_required

import lib.response.response as response
from application import db
from application.location.constants import *
from application.location.forms import LocationEditForm, LocationForm
from application.location.models import Location
from lib.decorators import load_location_by_id
from lib.response.constants import *


@jwt_required()
def create():
    form = LocationForm()

    if form.validate():
        location_data = {
            'name': form.name.data,
            'address': form.address.data,
            'retailer_id': current_user.id
        }
        location = Location(**location_data)

        db.session.add(location)
        db.session.commit()
        response_data = {'id': location.id}
        return response.success(status_code=RESOURCE_CREATED, data=response_data, message=LOCATION_CREATED)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


@jwt_required()
def get_all():
    locations = [location.to_dict() for location in current_user.locations]

    return response.success(status_code=REQUEST_COMPLETED, data=locations, message=ALL_LOCATIONS)


@jwt_required()
@load_location_by_id
def get_by_id(location):
    return response.success(status_code=REQUEST_COMPLETED, data=location.to_dict(), message=LOCATION)


@jwt_required()
@load_location_by_id
def update_by_id(location):
    form = LocationEditForm()

    if form.validate():
        form_address = form.address.data
        if form_address != location.address:
            location.description = form_address

            db.session.add(location)
            db.session.commit()
        response_data = {'address': form_address}
        return response.success(status_code=REQUEST_COMPLETED, data=response_data, message=LOCATION_UPDATED)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


@jwt_required()
@load_location_by_id
def delete_by_id(location):
    db.session.delete(location)
    db.session.commit()
    return response.success(status_code=REQUEST_COMPLETED, data=location.to_dict(), message=LOCATION_DELETED)
