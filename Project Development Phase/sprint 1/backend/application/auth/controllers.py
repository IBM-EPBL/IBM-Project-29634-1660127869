from application import db
from application.auth.forms import RegistrationForm, LoginForm
from application.auth.models import Retailer
from lib.response import Response


def register():
    form = RegistrationForm()
    if form.validate():
        retailer_data = {}
        retailer_data['name'] = form.name.data
        retailer_data['email'] = form.email.data
        retailer_data['address'] = form.address.data
        retailer = Retailer(**retailer_data)
        retailer.set_password(form.password.data)
        db.session.add(retailer)
        db.session.commit()
        return Response.success(data=retailer.id)
    return Response.error(data=form.errors, error_code=500)


def login():
    form = LoginForm()
    if form.validate():
        retailer = Retailer.query.filter_by(name=form.name.data).first()
        if retailer is None or not retailer.check_password(form.password.data):
            return Response.error(data='login error', error_code=500)
        return Response.success(data='login success', error_code=500)
    return Response.error(data=form.errors, error_code=500)
