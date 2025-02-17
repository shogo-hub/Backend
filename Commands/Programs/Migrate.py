from ..Argument import Argument
from ..AbstractCommand import AbstractCommand
from ...Database.MySQLWrapper import MySQLWrapper
import re
from typing import List, Optional
import os
import glob

class Migration(AbstractCommand):
    """Manage migration"""
    #STEP0: Set alias for command prompt
    alias = 'migrate'

    def __init__(self,arguments:dict):
        self.arguments = arguments
        
    @staticmethod
    def getArguments()->list:
        """Get argument of roll back"""
        return [
            Argument('rollback').description('Roll backwards. An integer n may also be provided to rollback n times.').required(False).allowAsShort(True),
            Argument('init').description("Create the migrations table if it doesn't exist.").required(False).allowAsShort(True),
        ]
    
    def execute(self)->int:
        """Execute migration based on command"""
        #STEP1 : Get mapped command of rollback
        rollback = self.getArgumentValue('rollback')

        #If state is init, create table from scratch
        if self.getArgumentValue("init"):
            self.createMigrationTable()

        #STEP2 : execute command
        if rollback is None:
            self.log("Starting migration......")
            self.migrate()
        else:
            rollbackNum = 1 if rollback is True else int(rollback)
            self.log("Running rollback....")

            self.rollback(rollbackNum)
        return 0    

    def createMigrationsTable(self):
        """Create scratch migration table"""

        print("Creating migrations table if necessary...")
        mysqli = MySQLWrapper()        
        result = mysqli.query("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255) NOT NULL
            );
        """)

        if result is False:  # Check for query failure
            raise Exception("Failed to create migration table.")

        print("Done setting up migration tables.")
    
    #STEP2: Migrate creation
    def migrate(self)->None:
        """Implement migration"""

        #Step1:Get all of migration info
        lastMigration = self.getLastMigration()
        all_migrations = self.getAllMigrationFiles()
        startIndex = all_migrations.index(lastMigration) + 1 if lastMigration else 0

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

            self.processQueries(queries)
            self.insertMigration(fileName)

        self.log("Migration ended...\n")   
    

    def log(self,message:str)->None:
        print(message)       
    

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

    #subClass------------------------------------------------------------------------------------------------

    def getClassNameFromMigrationFilename(self,filename:str)->str:
        match = re.search(r'([^_]+)\.py$', filename)
        if match:
            return f"Database.Migrations.{match.group(1)}"  # Python style namespace
        else:
            raise Exception("Unexpected migration filename format: " + filename)

    def getLastMigration(self) -> str:
        """Get last migration table"""
        mysqli = MySQLWrapper()
        query = "SELECT filename FROM migrations ORDER BY id DESC LIMIT 1"
        result = mysqli.query(query)

        if result and result.num_rows > 0:
            row = result.fetch_assoc()
            return row['filename']

        return None
    

    def getAllMigrationFiles(self, order: str = 'asc') ->list:
        """Get list of all of migration file path"""

        directory = os.path.join(os.path.dirname(__file__), "../../Database/Migrations") # Use os.path
        self.log(directory)
        allFiles = glob.glob(directory + "/*.py")
        #Sort file path by day 
        allFiles.sort(reverse=(order == 'desc'))
        return allFiles
    
    def processQueries(self, queries: List[str]) -> None:
        """Process multiple querries"""

        mysqli = MySQLWrapper()

        for query in queries:
            result = mysqli.query(query)
            if result is False:
                raise Exception(f"Query {{{query}}} failed.")
            else:
                self.log('Ran query: ' + query)

    def insertMigration(self, filename: str) -> None:
        """Insert migration record into the 'Migration table' """

        mysqli = MySQLWrapper()
        statement = mysqli.prepare("INSERT INTO migrations (filename) VALUES (?)")
        if not statement:
            raise Exception(f"Prepare failed: ({self.mysql.errno}) {self.mysql.error}")

        statement.bind_param("s", filename)

        if not statement.execute():
            raise Exception(f"Execute failed: ({statement.errno}) {statement.error}")
        statement.close()


    def rollback(self,times=1):
        self.log(f"Rolling back {times} migration(s)...")
