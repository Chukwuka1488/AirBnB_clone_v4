#!/usr/bin/python3
""" holds class User"""
from hashlib import md5
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        """Getter for the password attribute"""
        return self.__password

    @password.setter
    def password(self, pwd):
        """Setter for the password attribute, hashes the password to a MD5 value"""
        self.__password = md5(pwd.encode()).hexdigest()


    def __init__(self, *args, **kwargs):
        """initializes user"""
        pwd = kwargs.pop("password", None)
        super().__init__(*args, **kwargs)
        if pwd:
            self.password = pwd
