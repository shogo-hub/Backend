from abc import ABC, abstractmethod
from typing import List

class Command(ABC):
    """Interface for all commands to have """


    @staticmethod
    @abstractmethod
    def get_alias() -> str:
        """
        Return the alias for the command.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_arguments() -> List['Argument']:
        """
        Return a list of Argument objects.
        """
        pass
    
    @staticmethod
    @abstractmethod
    def get_help() -> str:
        """
        Return the help text for the command.
        """
        pass

    @staticmethod
    @abstractmethod
    def is_command_value_required() -> bool:
        """
        Return True if command value is required, False otherwise.
        """
        pass

    @abstractmethod
    def get_argument_value(self, arg: str) -> bool or str:
        """
        Return the argument value as a string if it exists,
        or True if the parameter is present, or False if the argument is not set.
        """
        pass

    @abstractmethod
    def execute(self) -> int:
        """
        Execute the command and return an integer (status code).
        """
        pass