from ..Argument import Argument
from ..AbstractCommand import AbstractCommand
from ...Database.MySQLWrapper import MySQLWrapper
import re
from typing import List, Optional
import os
import glob

class Migration:
    """Manage migration"""
    #STEP0: Set alias for command prompt
    alias = 'migrate'

    def __init__(self,arguments:dict):
        self.arguments = arguments
        self.mysql = MySQLWrapper()  # Initialize MySQLWrapper here

    @staticmethod
    def getArguments():
        """Get argument of roll back"""
        return [
            Argument('rollback').description('Roll backwards. An integer n may also be provided to rollback n times.').required(False).allowAsShort(True),
            Argument("init").description("Create the migrations table if it doesn't exist.").required(False).allowAsShort(True),
        ]
    #STEP0: Manage out of command
    def execute(self):
        """Based on Command manage migration"""

        rollback = self.getArgumentValue('rollback')
        
        #+++If command is creating migration table+++
        if self.getArgumentValue("init"):
            self.createMigrationTable()

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


    def log(self,message:str)->None:
        print(message)


        
    #STEP2: Migrate creation
    def migrate(self)->None:
        """Implement migration"""

        #Step1:Get all of migration info
        last_migration = self.get_last_migration()
        all_migrations = self.get_all_migration_files()
        start_index = all_migrations.index(last_migration) + 1 if last_migration else 0

        #Execute the migration which is not implemented yet
        for fileName in all_migrations:
            #Dynamically import the migration class
            moduleName = fileName[:-3].replace('/', '.').replace('\\', '.')
            module = __import__(moduleName, fromlist=['*'])
            className = self.getClassNameFromMigrationFilename(fileName)
            migrationClass = getattr(module, className.split('.')[-1])
            migration = migrationClass()

            self.log(f"Processing up migration for {migrationClass.__name__}")
            queries = migration.up()

            if not queries:
                raise Exception("Must have queries to run for ." + migrationClass.__name__)

            self.process_queries(queries)
            self.insert_migration(fileName)

        self.log("Migration ended...\n")

    #STEP3 Create migration table
    def createMigrationTable(self):
        """Create migration table"""
        self.log("Creating migrations table if necessary...")

        mysql = MySQLWrapper()

        query = """
            CREATE TABLE IF NOT EXISTS migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) NOT NULL
            );
        """

        result = mysql.querry(query)

        if result is False:
            raise Exception("Failed to create migration table.")

        self.log("Done setting up migration tables.")

    #subClass

    def getClassNameFromMigrationFilename(self,filename:str)->str:
        match = re.search(r'([^_]+)\.py$', filename)
        if match:
            return f"Database.Migrations.{match.group(1)}"  # Python style namespace
        else:
            raise Exception("Unexpected migration filename format: " + filename)

    def getLastMigration(self) -> Optional[str]:
        query = "SELECT filename FROM migrations ORDER BY id DESC LIMIT 1"
        result = self.mysql.query(query)

        if result and result.num_rows > 0:
            row = result.fetch_assoc()
            return row['filename']

        return None
    

    def getAllMigrationFiles(self, order: str = 'asc') -> List[str]:
        directory = os.path.join(os.path.dirname(__file__), "../../Database/Migrations") # Use os.path
        self.log(directory)
        all_files = glob.glob(directory + "/*.php")  # Use glob

        all_files.sort(reverse=(order == 'desc')) # Use list.sort with reverse argument

        return all_files
    
    def processQueries(self, queries: List[str]) -> None:
        for query in queries:
            result = self.mysql.query(query)
            if result is False:
                raise Exception(f"Query {{{query}}} failed.")
            else:
                self.log('Ran query: ' + query)

    def insert_migration(self, filename: str) -> None:
        statement = self.mysql.prepare("INSERT INTO migrations (filename) VALUES (?)")
        if not statement:
            raise Exception(f"Prepare failed: ({self.mysql.errno}) {self.mysql.error}")

        statement.bind_param("s", filename)

        if not statement.execute():
            raise Exception(f"Execute failed: ({statement.errno}) {statement.error}")


