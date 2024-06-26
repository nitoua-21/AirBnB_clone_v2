#!/usr/bin/python3
""" Amenicity Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from models.place import place_amenity
from sqlalchemy import Column, String
from sqlalchemy.orm import Relationship


class Amenity(BaseModel, Base):
    """Amenity Clss definition"""
    __tablename__ = 'amenities'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        place_amenities = Relationship("Place", secondary=place_amenity,
                                       back_populates='amenities')

    else:
        name = ""
