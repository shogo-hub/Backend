from ..Argument import Argument
from ..AbstractCommand import AbstractCommand
import os
import time
from datetime import datetime


class CodeGeneration(AbstractCommand):
    """Generate"""
    # Set the alias for the command
    alias = 'code-gen'
    requiredCommandValue = True

    #Get argument
    @staticmethod
    def getArguments()->list:
        return [
            Argument('name').description('Name of the file that is to be generated.').required(False),
        ]

    #Execute
    def execute(self):
        #Get command
        codeGenType = self.getCommandValue()#get_command_value()
        #Create migration ,if migration
        self.log(f'Generating code for.......{codeGenType}')
        #Implement rollback , if rollback
        if codeGenType =="migration":
            migrationName = self.getArgumentValue(arg="name")
            self.generateMigrationFile(migrationName)
        #Generate migration file

    def generateMigrationFile(self, migrationName: str) -> None:
        filename = f"{datetime.now().strftime('%Y-%m-%d')}_{int(time.time())}_{migrationName}.py"
        migrationContent = self.getMigrationContent(migrationName)

        # Define the path to save the migration file
        path = os.path.join(os.path.dirname(__file__), "../../Database/Migrations", filename)

        with open(path, 'w') as f:
            f.write(migrationContent)
        
        self.log(f"Migration file {filename} has been generated!")

    
    def getMigrationContent(self, migrationName: str) -> str:
        className = self.pascalCase(migrationName)
        return f"""# Generated Migration File

from Database.Migrations import SchemaMigration

class {className}(SchemaMigration):
    def up(self) -> list:
        # Add migration logic here
        return []

    def down(self) -> list:
        # Add rollback logic here
        return []
"""

    def pascalCase(self, string: str) -> str:
        return ''.join(word.capitalize() for word in string.split('_'))


    #NOTE:over ride below method because of nature of python (cannot overwrite to access concrete class variable)    
    @staticmethod
    def getHelp() -> str:
        help_string = f"Command: {CodeGeneration.getAlias()}"
        if CodeGeneration.isCommandValueRequired():
            help_string += " {value}"
        help_string += "\n"

        arguments:Argument = CodeGeneration.getArguments()
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
        return CodeGeneration.alias if CodeGeneration.alias else CodeGeneration.__name__
    
    @staticmethod
    def isCommandValueRequired() -> bool:
        return CodeGeneration.requiredCommandValue

    def getCommandValue(self) -> str:
        return CodeGeneration.argsMap.get(self.getAlias(), "")  

    
    

    
    

