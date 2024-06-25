#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.id = str(uuid.uuid4())
        else:
            if 'created_at' not in kwargs.keys():
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs.keys():
                self.updated_at = datetime.now()
            if 'id' not in kwargs.keys():
                self.id = str(uuid.uuid4())
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.to_dict())

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        from models import storage
        dict_repr = self.__dict__.copy()

        if type(storage).__name__ == 'FileStorage':
            dict_repr['__class__'] = self.__class__.__name__
            dict_repr['created_at'] = self.created_at.isoformat()
            dict_repr['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dict_repr:
            dict_repr.pop('_sa_instance_state')
        return dict_repr

    def delete(self):
        """Delete the current instance of the storage"""
        from models import storage
        key = f'{type(self).__name}.{self.id}'
        if key in storage.all():
            del storage.all()[key]
            storage.save()
