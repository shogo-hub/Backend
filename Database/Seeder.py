from abc import ABC , abstractmethod


class Seeder:
    """Interface of seeder for test"""

    @abstractmethod
    def seed(self)->None:
        """This is the method to handle the seeding processs"""
        pass

    @abstractmethod
    def createRowData(self):
        """This method will create row data to be seeded."""

        pass
