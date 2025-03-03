from .Command import Command
import sys
import json
from abc import ABC, abstractmethod
from .Argument import Argument

class AbstractCommand(Command):
    """Abstract command class for all of command"""
    #Initialize class value
    alias: str = None
    value: str = None
    argsMap: dict = {}
    requiredCommandValue: bool = False

    def __init__(self):
        #Map command line
        self.setUpArgsMap()     
        
    def setUpArgsMap(self):
        """Create map out of command"""

        #STEP1: Handling the Command Value
        args = sys.argv
        try:
            startIndex = args.index(self.getAlias())
        except ValueError:
            raise Exception(f"Could not find alias {self.getAlias()}")
        #Get the index of class name
        startIndex += 1

        #STEP2: Parsing Shell Arguments

        #Check if command is valid shape
        shellArgs = {}
        #If 
        if startIndex >= len(args) or args[startIndex].startswith('-'):
            if self.isCommandValueRequired():
                raise Exception(f"{self.getAlias()}'s value is required.")
        else:
            self.argsMap[self.getAlias()] = args[startIndex]
            startIndex += 1
        #Map optional command
        index = startIndex
        while index < len(args):
            arg = args[index]

            if arg[:2] == '--':
                key = arg[2:]
            elif arg[0] == '-':
                key = arg[1:]
            else:
                raise Exception('Options must start with - or --')

            shellArgs[key] = True

            #If next command exist, go to next optional argument name
            if index + 1 < len(args) and args[index + 1][0] != '-':
                shellArgs[key] = args[index + 1]
                index += 2
            else:
                shellArgs[key] = True
                index +=1
                  
        
        
        #STEP3: Check if shellArgs expected shape or not
        for argument in self.getArguments():
            #Get expected option
            argString = argument.getArgument()
            value = None

            if argument.isShortAllowed() and argString[0] in shellArgs:
                value = shellArgs[argString[0]]
            elif argString in shellArgs:
                value = shellArgs[argString]

            if value is None:
                if argument.isRequired():
                    raise Exception(f'Could not find the required argument {argString}')
                else:
                    self.argsMap[argString] = False
            else:
                self.argsMap[argString] = value

        self.log(json.dumps(self.argsMap))

    @staticmethod
    def getHelp() -> str:
        help_string = f"Command: {AbstractCommand.getAlias()}"
        if AbstractCommand.isCommandValueRequired():
            help_string += " {value}"
        help_string += "\n"

        arguments:Argument = AbstractCommand.getArguments()
        if not arguments:
            return help_string
 
        help_string += "Arguments:\n"

        for i in range(len(arguments)):
            argument:Argument = arguments[i]
            help_string += f"  --{argument.getArgument()}"
            if argument.isShortAllowed():
                help_string += f" (-{argument.getArgument()[0]})"
            help_string += f": {argument.getDescription()}"
            help_string += " (Required)" if argument.isRequired() else " (Optional)"
            help_string += "\n"
        return help_string

    @staticmethod
    def getAlias() -> str:
        """Return alis , else class name"""
        return AbstractCommand.alias if AbstractCommand.alias else AbstractCommand.__name__

    @staticmethod
    def isCommandValueRequired() -> bool:
        return AbstractCommand.requiredCommandValue

    def getCommandValue(self) -> str:
        return AbstractCommand.argsMap.get(self.getAlias(), "")

    def getArgumentValue(self, arg: str):
        """Return mapped argument"""
        return self.argsMap.get(arg, False)

    def log(self, info: str):
        print(info)

    @staticmethod
    @abstractmethod
    def getArguments()->list:
        """Return arguments"""

    @abstractmethod
    def execute(self) -> int:
        pass