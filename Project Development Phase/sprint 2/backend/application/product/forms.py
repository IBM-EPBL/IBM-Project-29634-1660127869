from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from application.product.models import Product


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])

    def validate_product_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product is not None:
            raise ValidationError('Product already exists!')


class ProductEditForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
