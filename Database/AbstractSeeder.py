from .MySQLWrapper import MySQLWrapper
from abc import ABC,abstractmethod

class AbstractSeeder(ABC):
    
    def __init__(self):
        super().__init__()
        self.mysqli = MySQLWrapper()
        self.tableName = None

    def Seed(self)->None:
        """This is the method to handle the seeding processs"""
        #Create
    def createRowData(self):
