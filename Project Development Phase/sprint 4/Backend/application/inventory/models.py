from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from application import db


class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'
    __table_args__ = (UniqueConstraint(
        'product_id', 'location_id', name='inventory_unique_product_id_location_id'), )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    threshold = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True,
                        default=datetime.now, onupdate=datetime.now)
    product = relationship('Product', back_populates='inventory_items')
    location = relationship('Location', back_populates='inventory_items')

    serialize_only = ('id', 'product.name', 'location.name', 'quantity', 'threshold')
