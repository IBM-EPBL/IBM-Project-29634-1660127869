import json

from application import create_app, db
from application.auth.models import Retailer
from application.location.models import Location
from application.product.models import Product

app = create_app()


# To Create Data For Development Purposes
def create_retailers():
    retailer_data = [
        {
            'name': 'John',
            'email': 'john@co.com',
            'is_active': False,
            'address': 'Compact'
        },
        {
            'name': 'John',
            'email': 'john@com.com',
            'is_active': True,
            'address': 'Madinson'
        }
    ]
    for data in retailer_data:
        retailer = Retailer(**data)
        retailer.set_password('password')
        db.session.add(retailer)
        db.session.commit()
        create_products(retailer.id)
        create_locations(retailer.id)


def create_products(retailer_id):
    produt_data = [
        {
            'name': 'product-1',
            'description': 'product-1 desc'
        },
        {
            'name': 'product-2',
            'description': 'product-2 desc'
        },
        {
            'name': 'product-3',
            'description': 'product-3 desc'
        }
    ]
    for data in produt_data:
        product = Product(retailer_id=retailer_id, **data)
        db.session.add(product)
        db.session.commit()


def create_locations(retailer_id):
    location_data = [
        {
            'name': 'location-1',
            'address': 'location-1 addr'
        },
        {
            'name': 'location-2',
            'address': 'location-2 addr'
        },
        {
            'name': 'location-3',
            'address': 'location-3 addr'
        }
    ]
    for data in location_data:
        location = Location(retailer_id=retailer_id, **data)
        db.session.add(location)
        db.session.commit()


@app.cli.command('create-db')
def create_db_data():
    try:
        db.drop_all()
        db.create_all()
        create_retailers()
    except Exception as e:
        print(e)
    finally:
        retailers = Retailer.query.all()
        for retailer in retailers:
            retailer = retailer.to_dict()
            print(json.dumps(retailer, indent=4, sort_keys=True))


if __name__ == '__main__':
    app.run()
