from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from application import db


class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'
    __table_args__ = (UniqueConstraint(
        'retailer_id', 'name', name='locations_unique_retailer_id_name'), )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    retailer_id = Column(Integer, ForeignKey('retailers.id'), nullable=False)
    name = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=True,
                        default=datetime.now, onupdate=datetime.now)
    retailer = relationship('Retailer', back_populates='locations')
    inventory_items = relationship(
        'Inventory', cascade='all, delete', back_populates='location')

    serialize_only = ('id', 'name', 'address')
