#!/usr/bin/python3
'''Contains the class DBStorage'''
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine as engine
from sqlalchemy.orm import scoped_session as session, sessionmaker as maker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    '''MySQL database'''
    __engine = None
    __session = None

    def __init__(self):
        '''DBStorage object'''
        hbnb_user = getenv('hbnb_user')
        hbnb_pwd = getenv('hbnb_pwd')
        hbnb_host = getenv('hbnb_host')
        hbnb_db = getenv('hbnb_db')
        hbnb_env = getenv('hbnb_env')
        self.__engine = engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                hbnb_user,
                                hbnb_pwd,
                                hbnb_host,
                                hbnb_db))
        if hbnb_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''list of objects of one type of class.'''
        n_dict = {}
        for cl_s in classes:
            if cls is None or cls is classes[cl_s] or cls is cl_s:
                objs = self.__session.query(classes[cl_s]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    n_dict[key] = obj
        return (n_dict)

    def new(self, obj):
        '''add the object'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes'''
        self.__session.commit()

    def reload(self):
        '''reloads data'''
        Base.metadata.create_all(self.__engine)
        ses_init = maker(bind=self.__engine, expire_on_commit=False)
        Session = session(ses_init)
        self.__session = Session

    def delete(self, obj=None):
        '''delete obj from __objects'''
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        '''close session'''
        self.__session.close()
