#!/usr/bin/python3
"""
Defines the HBNBCommand class
"""

import cmd
from signal import signal, SIGINT
from sys import exit
from models.base_model import BaseModel
import models
import shlex
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """
    enter and Entry point of the command interpreter
    """
    prompt = "(hbnb)"
    used_classes = [   #allowed_classes
        "BaseModel", "User", "State", "City", "Amenity", "Place", "Review"
        ]

    def quit(self, *args): #do_quit
        """Quit command to exit the program."""
        return True

    def EOF(self, *args): #do_EOF
        """Exit the program"""
        return True

    def empty_line(self): #emptyline
        """made Empty line"""
        pass

    def opertator(signal_received, frame): #handler
        """opertator the SIGINT or CTRL-C signal"""
        print("^C")
        exit(0)

    def maker_my(self, args):  #do_create
        """
        maker_my Create a new instance of a class
        """
        #Check if a class name is supplied as the argument.
        if len(args) == 0:
            self.error_hand_ler(1)
        else:
            args = args.split()
            if args[0] in self.used_classes:
                #Create a new instance of the class
                new_instance = eval(args[0])(args[1:])
                print(new_instance.id)
                new_instance.save()
            else:
                self.error_hand_ler(2)

    def de_display(self, args): #do_show
        """
         Prints the string representation of an instance based on the class name
        and id
        """
        if len(args) == 0:
            self.error_hand_ler(1)
        elif len(args) == 1:
            self.error_hand_ler(3)
        else:
            args = args.split()
            if args[0] in self.used_classes:
                models.storage.reload()
                #Create an identifier based on user input.
                identifier = args[0] + "." + args[1]
                if identifier in list(models.storage.all().keys()):
                    print(models.storage.all()[identifier])
                else:
                    self.error_hand_ler(4)
            else:
                self.error_hand_ler(2)


    def destoryer(self, args): #do_destroy
        """
        destroy or Deletes an instance based on the class name and id
        """
        args = args.split()
        if len(args) == 0:
            self.error_hand_ler(1)
        elif len(args) == 1:
            if args[0] in self.used_classes:
                self.error_hand_ler(3)
            else:
                self.error_hand_ler(2)
        else:
            if args[0] in self.used_classes:
                models.storage.reload()
                identifier = args[0] + "." + args[1]
                if identifier in list(models.storage.all().keys()):
                    del models.storage.all()[identifier]
                    models.storage.save()
                else:
                    self.error_hand_ler(4)
            else:
                self.error_hand_ler(2)


    def allerdo(self, args): #do_all
        """
        Prints all string representation of all instances
        based or not on the class name.
        """
        str_list = []
        #If length is zero, print all instances.
        if len(args) == 0:
            all_dict = models.storage.all()
            for id in all_dict.keys():
                obj = all_dict[id]
                str_list.append(str(obj))
            print(str_list)
        else:
            models.storage.reload()
            args = args.split()
            if args[0] in self.used_classes:
                all_dict = models.storage.all()
                for id in all_dict.keys():
                    if args[0] in id:
                        obj = all_dict[id]
                        str_list.append(str(obj))
                print(str_list)
            else:
                self.error_hand_ler(2)


    def updater(self, args): #do_update
        """
        for Updates an instance are based on the class name and id
        by adding
        """
        args = shlex.split(args)
        if len(args) == 0:
            self.error_hand_ler(1)
        elif len(args) == 1:
            if args[0] in self.used_classes:
                self.error_hand_ler(3)
            else:
                self.error_hand_ler(2)
        else:
            if args[0] in self.used_classes:
                models.storage.reload()
                identifier = args[0] + "." + args[1]
                if identifier in list(models.storage.all().keys()):
                    if len(args) == 2:
                        self.error_hand_ler(5)
                    elif len(args) == 3:
                        self.error_hand_ler(6)
                    else:
                        attr = args[2]
                        value = args[3]
                        setattr(models.storage.all()[identifier],attr, value)
                        models.storage.all()[identifier].save()
                else:
                    self.error_hand_ler(4)
            else:
                self.error_hand_ler(2)





    def error_hand_ler(self, error_num): #err_handler
        """For Handling errors in the progrm"""
        if error_num == 1:
            print("** class name missing **")
        elif error_num == 2:
            print("** class doesn't exist **")
        elif error_num == 3:
            print("** instance id missing **")
        elif error_num == 4:
            print("** no instance found **")
        elif error_num == 5:
            print("** attribute name missing **")
        elif error_num == 6:
            print("** value missing **")
if __name__ == "__main__":
    signal(SIGINT, HBNBCommand.handler)
    HBNBCommand().cmdloop()
    