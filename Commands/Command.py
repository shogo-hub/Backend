from abc import ABC, abstractmethod
from typing import List ,Union

class Command(ABC):
    """Interface for all commands to have"""

    @staticmethod
    @abstractmethod
    def getAlias() -> str:
        """
        Return the alias for the command.
        """
        pass

    @staticmethod
    @abstractmethod
    def getArguments() -> list:  # Changed to camelCase
        """
        Return a list of Argument objects.
        """
        pass

    @staticmethod
    @abstractmethod
    def getHelp() -> str:  # Changed to camelCase
        """
        Return the help text for the command.
        """
        pass

    @staticmethod
    @abstractmethod
    def isCommandValueRequired() -> bool:  # Changed to camelCase
        """
        Return True if command value is required, False otherwise.
        """
        pass

    @abstractmethod
    def getArgumentValue(self, arg: str) -> Union[bool,str]:  # Changed to camelCase
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