#!/usr/bin/python3
"""MySQL (sqlQlchemy) DB storage module"""
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """DB engine and query session manager definition"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        """Set up DB eengine with ENV variables"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}', pool_pre_ping=True)

        # Drop all tables in a "test" environment
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return all objects depending on 'cls' as a dictionary"""
        obj_dict = {}

        if cls is not None:
            response = self.__session.query(cls)
            for data in response:
                key = f"{type(data).__name__}.{data.id}"
                obj_dict[key] = data
        else:
            all_object = [User, State, Amenity, Place, Review]
            for obj in all_object:
                response = self.__session.query(obj)
                for data in response:
                    key = f"{type(data).__name__}.{data.id}"
                    obj_dict[key] = data

        return(obj_dict)

    def new(self, obj):
        """Add obj to current DB session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to current DB session"""
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the DB"""
        Base.metadata.create_all(self.__engine)
        newSession = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = newSession()
