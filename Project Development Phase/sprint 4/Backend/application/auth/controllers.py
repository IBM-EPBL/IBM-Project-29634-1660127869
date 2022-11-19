from datetime import datetime

from flask_jwt_extended import create_access_token

import lib.response.response as response
from application import db
from application.auth.constants import *
from application.auth.forms import (LoginForm, RegistrationForm,
                                    ResendConfirmationMailForm)
from application.auth.models import Retailer
from lib.mailer import send_confirmation_email
from lib.response.constants import *


def register():
    form = RegistrationForm()

    if form.validate():
        retailer_data = {
            'name': form.name.data,
            'email': form.email.data,
            'address': form.address.data,
            'is_active': False
        }
        retailer = Retailer(**retailer_data)
        retailer.set_password(form.password.data)

        send_confirmation_email(retailer)

        db.session.add(retailer)
        db.session.commit()
        response_data = {'id': retailer.id}
        return response.success(status_code=RESOURCE_CREATED, data=response_data, message=REGISTRATION_SUCCESS)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


def login():
    form = LoginForm()

    if form.validate():
        retailer = Retailer.query.filter_by(email=form.email.data).scalar()

        if retailer is None or (not retailer.check_password(form.password.data)):
            return response.error(status_code=UNAUTHORIZED_ACCESS, message=INVALID_DATA)
        elif not retailer.is_active:
            return response.error(status_code=UNAUTHORIZED_ACCESS, message=NOT_ACTIVE)

        access_token = create_access_token(retailer)
        response_data = {
            'jwt_token': access_token
        }
        return response.success(status_code=REQUEST_COMPLETED, data=response_data, message=LOGIN_SUCCESS)

    return response.error(status_code=UNPROCESSABLE_ENTITY, data=form.errors, message=INVALID_DATA)


def confirm_email(token):
    email = Retailer.verify_confirmation_token(token)

    if email:
        retailer = Retailer.query.filter_by(email=email).first()
        if not retailer.is_active:
            retailer.is_active = True
            retailer.email_confirmed_at = datetime.now()

            db.session.add(retailer)
            db.session.commit()
        response_data = {'id': retailer.id}
        return response.success(status_code=REQUEST_COMPLETED, data=response_data, message=ACCOUNT_CONFIRMED)

    response_data = {'token': token}
    return response.error(status_code=UNPROCESSABLE_ENTITY, data=response_data, message=INVALID_CONFIRMATION_TOKEN)


def resend_confirmation_email():
    form = ResendConfirmationMailForm()

    if form.validate():
        retailer = Retailer.query.filter_by(email=form.email.data).first()

        if not retailer:
            message = CONFIRMATION_MAIL_SENT
        elif retailer.is_active:
            message = ALREADY_CONFIRMED
        elif retailer.is_eligible_for_confirmation_resend():
            send_confirmation_email(retailer)
            retailer.confirmation_email_sent_at = datetime.now()

            db.session.add(retailer)
            db.session.commit()

            message = CONFIRMATION_MAIL_SENT
        else:
            message = WAIT_TO_GET_CONFIRMATION_MAIL

        return response.success(status_code=REQUEST_COMPLETED, message=message)

    return response.error(status_code=UNPROCESSABLE_ENTITY, message=INVALID_DATA)
