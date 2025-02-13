from ..Argument import Argument
from ..AbstractCommand import AbstractCommand


class Migration:
    """Manage migration"""
    #STEP0: Set alias for command prompt
    alias = 'migrate'


    @staticmethod
    def getArguments():
        """Get argument of roll back"""
        return [
            Argument('rollback').description('Roll backwards. An integer n may also be provided to rollback n times.').required(False).allowAsShort(True),
        ]

    #STEP0: Manage out of command
    def execute(self):
        """Based on Command manage migration"""

        rollback = self.getArgumentValue('rollback')
        if rollback is False:
            self.log("Starting migration......")
            self.migrate()
        else:
            # If rollback is set, either as True or with an integer value
            rollback = 1 if rollback is True else int(rollback)
            self.log("Running rollback....")
            for i in range(rollback):
                self.rollback()

        return 0  

    #STEP1: Rollback
    def rollback(self):
        self.log("Rolling back migration...\n")


    #STEP2: Migrate creation
    def migrate(self):
        self.log("Running migrations...")
        self.log("Migration ended...\n")


