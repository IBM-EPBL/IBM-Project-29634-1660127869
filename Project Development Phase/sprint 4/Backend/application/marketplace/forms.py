from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from application.location.models import Location
from application.product.models import Product


class PurchaseOrderForm(FlaskForm):
    product_name = StringField('Product_Name', validators=[DataRequired()])
    location_name = StringField('Location_Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
                            NumberRange(min=1, max=9999)])

    def validate_product_name(self, name):
        product = Product.query.filter_by(name=name.data).scalar()
        if product is None:
            raise ValidationError('Product doesn\'t exist!')

    def validate_location_name(self, name):
        location = Location.query.filter_by(name=name.data).scalar()
        if location is None:
            raise ValidationError('Location doesn\'t exist!')
