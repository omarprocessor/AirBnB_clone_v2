#!/usr/bin/python3
"""
Command interpreter for managing objects in the HBNB project.
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Command interpreter class """
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_quit(self, args):
        """ Quit the program """
        return True

    def do_EOF(self, args):
        """ Exit the program """
        print()
        return True

    def emptyline(self):
        """ Do nothing on empty line input """
        pass

    def do_create(self, args):
        """ Create an object of any class with given parameters """
        if not args:
            print("** class name missing **")
            return

        # Split class name and parameters
        args = args.split()
        class_name = args[0]

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Create an instance of the class
        new_instance = HBNBCommand.classes[class_name]()

        for param in args[1:]:
            if '=' not in param:
                continue

            key, value = param.split('=', 1)

            # Process the value
            if value.startswith('"') and value.endswith('"'):
                # String: replace underscores and handle escaped quotes
                value = value[1:-1].replace('_', ' ').replace('\\"', '"')
            elif '.' in value:  # Float
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:  # Integer
                try:
                    value = int(value)
                except ValueError:
                    continue

            # Set the attribute
            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """ Show an object by class name and ID """
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        print(storage.all()[key])

    def do_destroy(self, args):
        """ Destroy an object by class name and ID """
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        del storage.all()[key]
        storage.save()

    def do_all(self, args):
        """ Show all objects or all objects of a class """
        if args and args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        objs = storage.all()
        obj_list = [
            str(obj) for key, obj in objs.items()
            if not args or key.startswith(args + ".")
        ]
        print(obj_list)

    def do_update(self, args):
        """ Update an object by adding or updating an attribute """
        args = args.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]

        try:
            attr_value = eval(attr_value)
        except Exception:
            pass

        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
