from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from application.location.models import Location


class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    def validate_name(self, name):
        location = Location.query.filter_by(name=name.data).scalar()
        if location is not None:
            raise ValidationError('Location already exists!')


class LocationEditForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
