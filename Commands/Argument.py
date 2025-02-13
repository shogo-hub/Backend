from abc import ABC, abstractmethod
from typing import List



class Argument:
    """Define the argument for the command to use"""
    def __init__(self, argument: str):
        self.argument = argument
        self.description = ''
        self.required = True
        self.allow_as_short = False

    def get_argument(self) -> str:
        """Returns the argument name."""
        return self.argument

    def get_description(self) -> str:
        """Returns the description of the argument."""
        return self.description

    def description(self, description: str) -> 'Argument':
        """Sets the description of the argument and returns the current instance."""
        self.description = description
        return self

    def is_required(self) -> bool:
        """Returns whether the argument is required."""
        return self.required

    def required(self, required: bool) -> 'Argument':
        """Sets whether the argument is required and returns the current instance."""
        self.required = required
        return self

    def is_short_allowed(self) -> bool:
        """Returns whether the argument can be used as a short form."""
        return self.allow_as_short

    def allow_as_short(self, allow_as_short: bool) -> 'Argument':
        """Sets whether the argument can be used as a short form and returns the current instance."""
        self.allow_as_short = allow_as_short
        return self
