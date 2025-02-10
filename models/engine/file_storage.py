#!/usr/bin/python3
"""
FileStorage class for serializing and deserializing objects
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity, "BaseModel": BaseModel, "City": City,
    "Place": Place, "Review": Review, "State": State, "User": User
}


class FileStorage:
    """Handles serialization and deserialization of objects to and from JSON"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns all stored objects or filtered
objects of a specific class"""
        if not cls:
            return self.__objects
        elif isinstance(cls, str):
            return {k: v for k, v in self.__objects.items()
                    if v.__class__.__name__ == cls}
        else:
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}

    def new(self, obj):
        """Adds a new object to storage"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes objects to the JSON file"""
        json_objects = {key: obj.to_dict(save_to_disk=True)
                        for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes objects from the JSON file"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Ignore errors if the file does not exist or is corrupted

    def delete(self, obj=None):
        """Deletes an object from storage"""
        if obj:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """Reloads objects from JSON storage"""
        self.reload()

    def get(self, cls, id):
        """Retrieves a single object by class and ID"""
        if cls and isinstance(cls, str) and id and isinstance(id, str) and cls in classes:
            return self.__objects.get(f"{cls}.{id}", None)
        return None

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        return len(self.all(cls))
