from abc import ABC, abstractmethod
from typing import List

class Argument:
    """Define the argument for the command to use"""
    def __init__(self, argument: str):
        self.argument = argument
        self.description = ''
        self.required = True
        self.allowAsShort = False  # Changed to camelCase

    def getArgument(self) -> str:  # Changed to camelCase
        """Returns the argument name."""
        
        return self.argument

    def getDescription(self) -> str:  # Changed to camelCase
        """Returns the description of the argument."""
        
        return self.description

    def setDescription(self, description: str) -> 'Argument':
        """Sets the description of the argument and returns the current instance."""
        
        self.description = description
        return self

    def isRequired(self) -> bool:  # Changed to camelCase
        """Returns whether the argument is required."""
        
        return self.required

    def setRequired(self, required: bool) -> 'Argument':
        """Sets whether the argument is required and returns the current instance."""
        
        self.required = required
        return self

    def isShortAllowed(self) -> bool:  # Changed to camelCase
        """Returns whether the argument can be used as a short form."""
        
        return self.allowAsShort  # Use the camelCase version

    def allowAsShort(self, allow_as_short: bool) -> 'Argument':  # Changed to camelCase
        """Sets whether the argument can be used as a short form and returns the current instance."""
        
        self.allowAsShort = allow_as_short  # Changed to camelCase
        return self