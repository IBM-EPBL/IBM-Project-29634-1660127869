from datetime import datetime

from flask_jwt_extended import create_access_token

from application import db
from application.auth.constants import *
from application.auth.forms import (LoginForm, RegistrationForm,
                                    ResendConfirmationMailForm)
from application.auth.models import Retailer
from lib.constants import *
from lib.mailer import send_confirmation_email
from lib.response import response
from lib.response_status_codes import *


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
        return response(status_code=RESOURCE_CREATED, status=SUCCESS, data=response_data, message=REGISTRATION_SUCCESS)

    return response(status_code=UNPROCESSABLE_ENTITY, status=ERROR, data=form.errors, message=INVALID_DATA)


def login():
    form = LoginForm()

    if form.validate():
        retailer = Retailer.query.filter_by(email=form.email.data).first()
        if retailer is None or (not retailer.check_password(form.password.data)):
            return response(status_code=UNAUTHORIZED_ACCESS, status=ERROR, message=INVALID_DATA)

        access_token = create_access_token(retailer)
        response_data = {
            'jwt_token': access_token
        }
        return response(status_code=REQUEST_COMPLETED, status=SUCCESS, data=response_data, message=LOGIN_SUCCESS)

    return response(status_code=UNPROCESSABLE_ENTITY, status=ERROR, data=form.errors, message=INVALID_DATA)


def confirm_email(token):
    email = Retailer.verify_confirmation_token(token)

    if email:
        retailer = Retailer.query.filter_by(email=email).first()
        retailer.is_active = True
        retailer.email_confirmed_at = datetime.now()

        db.session.add(retailer)
        db.session.commit()
        response_data = {'id': retailer.id}
        return response(status_code=REQUEST_COMPLETED, status=SUCCESS, data=response_data, message=ACCOUNT_CONFIRMED)

    response_data = {'token': token}
    return response(status_code=UNPROCESSABLE_ENTITY, status=ERROR, data=response_data, message=INVALID_CONFIRMATION_TOKEN)


def resend_confirmation_email():
    form = ResendConfirmationMailForm()

    if form.validate():
        retailer = Retailer.query.filter_by(email=form.email.data).first()

        if not retailer:
            message = CONFIRMATION_MAIL_SENT
        elif retailer.is_eligible_for_confirmation_resend():
            send_confirmation_email(retailer)
            retailer.confirmation_email_sent_at = datetime.now()

            message = CONFIRMATION_MAIL_SENT
        else:
            message = WAIT_TO_GET_CONFIRMATION_MAIL

        db.session.add(retailer)
        db.session.commit()
        return response(status_code=REQUEST_COMPLETED, status=SUCCESS, data={}, message=message)

    return response(status_code=UNPROCESSABLE_ENTITY, status=ERROR, data={}, message=INVALID_DATA)
