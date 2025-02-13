from ..Argument import Argument
from ..AbstractCommand import AbstractCommand



class CodeGeneration(AbstractCommand):
    """Generate """
    # Set the alias for the command
    alias = 'code-gen'
    requiredCommandValue = True

    @staticmethod
    def getArguments():
        return []

    def execute(self):
        codeGenType = self.getCommandValue()
        self.log(f'Generating code for....... {codeGenType}')
        return 0
    
    
