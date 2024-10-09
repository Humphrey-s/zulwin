#!/usr/bin/python3
import cmd
from models import storage
from models.base_model import BaseModel
import shlex
from models.user import User
from models.item import Item


classes = {"BaseModel": BaseModel, "User": User, "Item": Item}


class ZulwinCommand(cmd.Cmd):
    prompt = "(zulwin) "

    def key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, args):
        """Creates a new object:
            syntax: create Class keys=value
        """
        arg = args.split()
        if arg is None or len(arg) == 0:
            print("** class missing **")
        if arg[0] not in classes.keys():
            print("** class missing **")

        d_ct = self.key_value_parser(arg[1:])
        obj = classes[arg[0]](**d_ct)
        obj.save()
        print(obj.__class__.__name__ + ":  " + obj.id)


    def do_all(self, arg):
        """prints stored objects of a class"""
        args = arg.split()
        if len(args) == 0:
            objs = storage.all()
        else:
            if args[0] in classes.keys():
                objs = storage.all(classes[args[0]])
            else:
                print("** class missing **")
     
        [print(obj) for obj in objs.values()]

    def do_delete(self, arg):
        """deletes object"""
        args = arg.split()
        if len(args) == 0:
            print("** class missing**")
        elif len(args) < 2:
            print("** instance missing **")
        else:
            if args[0] in classes:
                objs = storage.all(classes[args[0]])

                for obj in objs.values():
                    if obj.id == args[1]:
                        obj.delete()
                        print("[]")
                        break
                else:
                    print("** instance not found **")
            else:
                print("** class missing **")

    def do_delete_all(self, arg):
        """delete all class objects"""
        args = arg.split()
        if len(args) == 0:
            print("** class missing**")
        elif len(args) < 1:
            print("** instance missing **")
        else:
            if args[0] in classes:
                objs = storage.all(classes[args[0]])

                for obj in objs.values():
                        obj.delete()
                else:
                    print("successful")
            else:
                print("** class missing **")


    def do_quit(self, arg):
        """quits the console"""
        print("Bye")
        quit()

if __name__ == "__main__":
    ZulwinCommand().cmdloop()