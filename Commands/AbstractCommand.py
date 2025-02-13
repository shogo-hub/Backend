from .Command import Command
import sys
import json
from abc import ABC, abstractmethod

class AbstractCommand(Command):
    """Abstract command class for all of command"""
    value: str = None
    args_map: dict = {}
    alias: str = None
    required_command_value: bool = False

    def __init__(self):
        self.set_up_args_map()

    def set_up_args_map(self):
        args = sys.argv
        start_index = None

        try:
            start_index = args.index(self.get_alias()) + 1
        except ValueError:
            raise Exception(f"Could not find alias {self.get_alias()}")

        shell_args = {}

        if start_index == len(args) or args[start_index][0] == '-':
            if self.is_command_value_required():
                raise Exception(f"{self.get_alias()}'s value is required.")
        else:
            self.args_map[self.get_alias()] = args[start_index]
            start_index += 1

        for i in range(start_index, len(args)):
            arg = args[i]
            if arg.startswith('--'):
                key = arg[2:]
            elif arg.startswith('-'):
                key = arg[1:]
            else:
                raise Exception('Options must start with - or --')

            shell_args[key] = True

            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                shell_args[key] = args[i + 1]
                i += 1

        for argument in self.get_arguments():
            arg_string = argument.get_argument()
            value = None

            if argument.is_short_allowed() and arg_string[0] in shell_args:
                value = shell_args[arg_string[0]]
            elif arg_string in shell_args:
                value = shell_args[arg_string]

            if value is None:
                if argument.is_required():
                    raise Exception(f"Could not find the required argument {arg_string}")
                else:
                    self.args_map[arg_string] = False
            else:
                self.args_map[arg_string] = value

        self.log(json.dumps(self.args_map))

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
    def get_alias() -> str:
        return static.alias if static.alias else static.__name__

    @staticmethod
    def is_command_value_required() -> bool:
        return static.required_command_value

    def get_command_value(self) -> str:
        return self.args_map.get(self.get_alias(), "")

    def get_argument_value(self, arg: str):
        return self.args_map.get(arg, False)

    def log(self, info: str):
        print(info)

    @abstractmethod
    def execute(self) -> int:
        pass