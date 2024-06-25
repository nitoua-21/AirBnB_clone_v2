#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import Relationship


class State(BaseModel, Base):
    """ State class """
    name = Column(String(128), nullable=False)
    __tablename__ = "states"
    cities = Relationship("City", cascade='delete', backref='state')
