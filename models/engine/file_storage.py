#!/usr/bin/python3
"""file storage engine"""
import json
import models
import os

class FileStorage():

    def __init__(self):
        self.__file = "file.json"
        self.__objects = {}

    def new(self, obj):
        """adds new object to self.__objects"""
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        self.__objects[key] = obj

    def all(self, cls=None):
        """retrieve stored objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.item import Item

        classes = {"BaseModel": BaseModel, "User": User, "Item": Item}
        new_dct = {}

        if cls is not None:
            for key, value in self.__objects.items():
                if cls is value.__class__:
                    new_dct[key] = value
            return new_dct
        else:
            return self.__objects

    def save(self):
        """save object to file"""
        new_dict = {}
        for key, obj in self.__objects.items():
            new_dict[key] = obj.to_dict()

        with open(self.__file, "w") as f:
            json.dump(new_dict, f)

    def reload(self):
        """stores objects in self.__objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.item import Item

        classes = {"BaseModel": BaseModel, "User": User, "Item": Item}

        if os.path.exists(self.__file):
            with open(self.__file, "r") as f:
                lst = json.load(f)
            for key, value in lst.items():
                d = value.copy()
                d.pop("__class__")
                self.__objects[key] = classes[value["__class__"]](**d)
                
        else:
            pass

    def update(self, obj, dct):
        """updates an object"""
        from models.base_model import BaseModel
        from models.user import User
        from models.item import Item

        classes = {"BaseModel": BaseModel, "User": User, "Item": Item}
        objs = self.__objects.copy()


        for key, ob in objs.items():
            key1 = ob.__class__.__name__ + "." + str(ob.id)
            if ob.id == obj.id:
                d = ob.to_dict()
                d_copy = ob.to_dict()
                class_name = d["__class__"]

                d_copy.pop("__class__")
                d_copy[dct["key"]] = dct["value"]
                updated_obj = classes[class_name](**d_copy)

                del self.__objects[key]
                self.__objects[key] = updated_obj
                self.save()

                return updated_obj.to_dict()
        else:
            return {"success": "None"}


    def delete(self, obj):
        """deletes an object"""
        objs = self.__objects.copy()
    
        for key, ob in objs.items():
            key1 = ob.__class__.__name__ + "." + str(ob.id)
            #print(f"{key}: {key1}")
            if ob.id == obj.id:
                del self.__objects[key]
                self.save()

    def get(self, object_id):
        """returns object with same id"""
        all_objects = self.all()

        for obj in all_objects.values():
            if obj.id == object_id:
                return obj
        else:
            return None