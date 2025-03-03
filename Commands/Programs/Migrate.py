from ..Argument import Argument
from ..AbstractCommand import AbstractCommand
from Database.MySQLWrapper import MySQLWrapper
import re
import inspect
from typing import List, Optional
import os
import glob
import importlib.util
from Database.Migrations.Migration_2025_02_20_1740020081_CreateUserTable1 import CreateUserTable1
import sys


class Migrate(AbstractCommand):
    """Manage migration"""
    #STEP0: Set alias for command prompt
    alias = 'migrate'

    def __init__(self):
        super().__init__()
        
    @staticmethod
    def getArguments()->list:
        """Get argument of roll back"""
        rollBack = Argument('rollback')
        rollBack.setDescription('Roll backwards. An integer n may also be provided to rollback n times.')
        rollBack.setRequired(False)
        rollBack.setAllowAsShort(allow_as_short=True)
        initOb = Argument('init')
        initOb.setDescription("Create the migrations table if it doesn't exist.")
        initOb.setRequired(False)
        initOb.setAllowAsShort(allow_as_short=True)

        return [
            rollBack,
            initOb
        ]
    
    def execute(self)->int:
        """Execute migration based on command"""
        #STEP1 : Get mapped command of rollback
        rollback = self.getArgumentValue('rollback')

        #If state is init, create table from scratch
        if self.getArgumentValue("init"):
            self.createMigrationTable()

        #STEP2 : execute command
        if rollback == None or rollback == False:
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
            absolutePath = os.path.abspath(fileName)
            className = self.getClassNameFromMigrationFilename(filename=absolutePath)
           

            moduleName = os.path.splitext(os.path.basename(absolutePath))[0]
            moduleSPec = importlib.util.spec_from_file_location(moduleName, absolutePath)
            module = importlib.util.module_from_spec(moduleSPec)
            moduleSPec.loader.exec_module(module)
            
            class_ = getattr(module, className)

            instance = class_()
            queries = instance.up()
            
            

        
            self.processQueries(queries=queries)          
            self.insertMigration(filename=absolutePath)

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

        result = mysql.query(query)

        if result is False:
            raise Exception("Failed to create migration table.")

        self.log("Done setting up migration tables.")

    def rollback(self,times=1)->None:
        """Roll back migration at user designated times"""
        
        self.log(f"Rolling back {times} migration(s)...")

        #STEP1 :Get Implemented migration data
        lastMigration = self.getLastMigration()
        allMigrations = self.getAllMigrationFiles()
        try:
            lastMigrationIndex = allMigrations.index(lastMigration)
        except ValueError:
            self.log("Could not find the last migration ran: " + lastMigration)
            return
        
        #STEP2 : Implement rollBack
        count = 0
        for i in range(lastMigrationIndex,-1,-1):
            if count >= times:
                break
            fileName = allMigrations[i]

            self.log(f"Rolling back: {fileName}")

            #Try to import python file
            try:
                spec = importlib.util.spec_from_file_location("migration_module", fileName)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                migrationClass = getattr(module, self.getClassNameFromMigrationFilename(fileName))
                migration = migrationClass()

                queries = migration.down()
                if not queries:
                    raise Exception("Must have queries to run for " + migrationClass.__name__)

                self.processQueries(queries)
                self.removeMigration(fileName)
                count += 1
            except FileNotFoundError:
                self.log(f"Error: Migration file {fileName} not found.")
            except AttributeError:
                self.log(f"Error: Class {self.getClassNameFromMigrationFilename(fileName)} not found in {fileName}.")
            except Exception as e:
                self.log(f"Error during rollback: {e}")
                break

    #subClass------------------------------------------------------------------------------------------------
    def load_class_from_file(self,file_path):
        """
        Loads a class from a Python file, assuming there's only one class defined.

        Args:
            file_path (str): The path to the Python file.

        Returns:
            type or None: The loaded class, or None if an error occurs.
        """
        try:
            # Get the module name and directory
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            module_dir = os.path.dirname(os.path.abspath(file_path))

            # Add the directory to sys.path temporarily
            sys.path.insert(0, module_dir)

            # Import the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Remove the directory from sys.path
            sys.path.pop(0)

            # Find the class in the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module.__name__:
                    return obj

            return None  # No class found

        except (ImportError, FileNotFoundError, AttributeError, Exception) as e:
            print(f"Error loading class: {e}")
            return None
    
    
    
    
    def removeMigration(self,fileName)->None:
        """Remove migration from migration table"""
        mysqli = MySQLWrapper()
        statement = "DELETE FROM migrations WHERE filename = ?"
        mysqli.query(sql=mysqli,params=(fileName))

        
    
    
    def getClassNameFromMigrationFilename(self,filename:str)->str:
        """Get class name out of file Path"""
        match = re.search(r'([^_]+)\.py$', filename)
        if match:
            return match.group(1)
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

    #TODO :  I will modify this code ,since I cannot use state or so 
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



    #NOTE:over ride below method because of nature of python (cannot overwrite to access concrete class variable)    
    @staticmethod
    def getHelp() -> str:
        help_string = f"Command: {Migrate.getAlias()}"
        if Migrate.isCommandValueRequired():
            help_string += " {value}"
        help_string += "\n"

        arguments:Argument = Migrate.getArguments()
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
        return Migrate.alias if Migrate.alias else Migrate.__name__

    @staticmethod
    def isCommandValueRequired() -> bool:
        return Migrate.requiredCommandValue

    def getCommandValue(self) -> str:
        return Migrate.argsMap.get(self.getAlias(), "")

