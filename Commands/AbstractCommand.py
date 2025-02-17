from .Command import Command
import sys
import json
from abc import ABC, abstractmethod

class AbstractCommand(Command):
    """Abstract command class for all of command"""
    

    def __init__(self):
        self.set_up_args_map()
        self.value: str = None
        self.argsMap: dict = {}
        self.alias: str = None
        self.requiredCommandValue: bool = False

    def setUpArgsMap(self):
        """Create map out of command"""

        #STEP1: Handling the Command Value
        args = sys.argv
        try:
            startIndex = args.index(self.getAlias()) +1
        except ValueError:
            raise Exception(f"Could not find alias {self.getAlias()}")
        startIndex = self.getAlias()


        #STEP2: Parsing Shell Arguments
        #Check if command is valid shape
        shellArgs = {}
        if not (startIndex < len(args) and args[startIndex][0] != '-'):
            if self.is_command_value_required():
                raise Exception(f"{self.getAlias()}'s value is required.")
        else:
            self.argsMap[self.getAlias()] = args[startIndex]
            startIndex += 1
        #Map optional command
        for i in range(startIndex, len(args)):
            arg = args[i]

            if arg[:2] == '--':
                key = arg[2:]
            elif arg[0] == '-':
                key = arg[1:]
            else:
                raise Exception('Options must start with - or --')

            shellArgs[key] = True

            if i + 1 < len(args) and args[i + 1][0] != '-':
                shellArgs[key] = args[i + 1]
                i += 1


        #STEP3: Check if shellArgs expected shape or not
        for argument in self.get_arguments():
            #Get expected option
            argString = argument.get_argument()
            value = None

            if argument.is_short_allowed() and argString[0] in shellArgs:
                value = shellArgs[argString[0]]
            elif argString in shellArgs:
                value = shellArgs[argString]

            if value is None:
                if argument.is_required():
                    raise Exception(f'Could not find the required argument {argString}')
                else:
                    self.argsMap[argString] = False
            else:
                self.argsMap[argString] = value

        self.log(json.dumps(self.argsMap))

    @staticmethod
    def get_help() -> str:
        help_string = f"Command: {static.get_alias()}"
        if static.is_command_value_required():
            help_string += " {value}"
        help_string += "\n"

        arguments = static.get_arguments()
        if not arguments:
            return help_string

        help_string += "Arguments:\n"

        for argument in arguments:
            help_string += f"  --{argument.get_argument()}"
            if argument.is_short_allowed():
                help_string += f" (-{argument.get_argument()[0]})"
            help_string += f": {argument.get_description()}"
            help_string += " (Required)" if argument.is_required() else " (Optional)"
            help_string += "\n"

        return help_string

    @staticmethod
    def getAlias() -> str:
        return self.alias if self.alias else self.__name__

    @staticmethod
    def is_command_value_required() -> bool:
        return self.requiredCommandValue

    def get_command_value(self) -> str:
        return self.argsMap.get(self.get_alias(), "")

    def get_argument_value(self, arg: str):
        return self.argsMap.get(arg, False)

    def log(self, info: str):
        print(info)

    @abstractmethod
    def execute(self) -> int:
        pass