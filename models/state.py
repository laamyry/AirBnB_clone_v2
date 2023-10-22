#!/usr/bin/python3
'''list of City objects from storage linked to the current State'''
import models
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
import sqlalchemy
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship as relat


class State(BaseModel, Base):
    '''state'''
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relat("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            list = []
            allcities = models.storage.all(City)
            for city in allcities.values():
                if city.state_id == self.id:
                    list.append(city)
            return list
