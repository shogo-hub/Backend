from ..Argument import Argument
from ..AbstractCommand import AbstractCommand
import os
import time
from datetime import datetime



class CodeGeneration(AbstractCommand):
    """Generate """
    # Set the alias for the command
    alias = 'code-gen'
    requiredCommandValue = True

    #Get argument
    @staticmethod
    def getArguments():
        return [
            Argument('name').description('Name of the file that is to be generated.').required(False),
        ]
    
    #Execute
    def execute(self):
        #Get command
        codeGenType = self.get_command_value()
        #Create migration ,if migration
        self.log(f'Generating code for.......{codeGenType}')
        #Implement rollback , if rollback
        if codeGenType =="migration":
            migrationName = self.get_argument_value(arg="name")
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

    
    
    

    
    

