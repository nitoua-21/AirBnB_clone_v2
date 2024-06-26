#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import Relationship
from models.review import Review


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60),  ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60),  ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = Relationship("Review", cascade='delete', backref='place')
        amenities = Relationship("Amenity",
                                 secondary=place_amenity, viewonly=False,
                                 back_populates="place_amenities")

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            '''
                Return list: review instances if Review.place_id==curr place.id
                FileStorage relationship between Place and Review
            '''
            from models import storage
            return [review for review in storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """
            Getter attribute amenities that returns the list
            of Amenity instances based on the attribute amenity_ids
            that contains all Amenity.id linked to the Place
            """
            from models import storage
            from models.amenity import Amenity

            return [amenity for amenity in storage.all(Amenity).values()
                    if amenity.place_id == self.id]

        @amenities.setter
        def amenities(self, amenity=None):
            """
            Setter attribute amenities that handles append method for adding
            an Amenity.id to the attribute amenity_ids.
            """
            from models.amenity import Amenity
            if amenity and isinstance(amenity, Amenity):
                if amenity.place_id == self.id:
                    self.amenity_ids.append(amenity.id)
