#!/usr/bin/python3
"""This module defines a class User"""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.base_model import BaseModel
from sqlalchemy.orm import Relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        places = Relationship("Place", cascade='delete', backref='user')
        reviews = Relationship("Review", cascade='delete', backref='user')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
