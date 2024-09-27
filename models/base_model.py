#!/usr/bin/python3
"""base model for echetra"""
from uuid import uuid4
from datetime import datetime


Tformat = "%Y-%m-%d %H:%M:%S"

class BaseModel():

    def __init__(self, *args, **kwargs):
        
        if kwargs is None:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow().strftime(Tformat)
            self.updated_at = datetime.utcnow().strftime(Tformat)
        else:

            for key, value in kwargs.items():
                setattr(self, key, value)
            if "id" not in kwargs.keys():
                self.id = str(uuid4())
                self.created_at = datetime.utcnow().strftime(Tformat)
                self.updated_at = datetime.utcnow().strftime(Tformat)
            else:
                self.id = str(uuid4())
                if "created_at" not in kwargs.keys():
                    self.created_at = datetime.now().strftime(Tformat)
                else:
                    self.updated_at = datetime.now().strftime(Tformat)
    
    def __str__(self):
        """prints string representation of basemodel"""
        dct = {}
        key = "(" + str(self.__class__.__name__) + "." + str(self.id) + ")"
        value = str(self.__dict__)
        dct[key] = value
        return str(dct)

    def to_dict(self):
        """returns JSON rep of an instance"""
        new_dct = self.__dict__
        new_dct["updated_at"] = datetime.now().strftime(Tformat)
        new_dct["created_at"] = datetime.now().strftime(Tformat)
        new_dct["__class__"] = self.__class__.__name__

        return new_dct

    def save(self):
        """saves an object to file or db"""
        from models import storage
        storage.new(self)
        storage.save()

    def delete(self):
        """delete obj"""
        from models import storage
        storage.delete(self)