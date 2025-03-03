from Exceptions.ReadAndParseEnvException import ReadAndParseEnvException
from configparser import ConfigParser
import os
from configparser import ConfigParser, NoSectionError,NoOptionError


class Settings:
    ENV_PATH = ".env"
    @staticmethod
    def env()->str:
        """Get the environment setting Correspoinding to pair key"""

        # Create a ConfigParser object
        config = ConfigParser()

        # Set the path to the .env file
        env_path = os.path.join(os.path.dirname(__file__), '..', Settings.ENV_PATH)

        # Read the .env file
        if not config.read(env_path):
            # Raise an exception if reading the file fails
            raise ReadAndParseEnvException(f"Failed to read {env_path}")


        # If 'pair' contains a dot, split it into section and option
        #if '.' in pair:
            #section, option = pair.split('.', 1)
        return config
    
        """
        try:
            # Retrieve the value from the specified section and option
            return config.get(section, option)
        except (NoSectionError, NoOptionError):
            # Raise an exception if the section or option does not exist
            raise ReadAndParseEnvException(f"'{pair}' not found in the environment file.")
        """