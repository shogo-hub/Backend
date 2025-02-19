import sys
import importlib
import pdb
import os



#php console {program} {program_value} {--option1} {option1_value} {--option2} {option2_value} ... {--optionN} {optionN_value}

def autoload(className):
    """Autoload classes from the 'Commands' directory."""
    #STEP1 :  get file name
    #
    filePath = os.path.join(os.path.dirname(__file__), 'Commands', className) # Changed to camelCase
    if os.path.exists(filePath): # Changed to camelCase
        moduleName = str(className).rsplit('.', 1)[0]
        try:
            module = importlib.import_module(moduleName) # Changed to camelCase
            return getattr(module, className.rsplit('.', 1)[1]) #Class object
        except (ImportError, AttributeError):
            raise Exception(f"Failed to import class: {className} from file: {filePath}")
    else:
        raise Exception(f"File not found: {filePath}")
    


def main()->int:
    """
    Entry point of Comamnd
    Expected command----->  python console {program} {programValue} {--option1} [option1_value]  .......
    python console code-gen migration --name CreateUsersTestTable1
     
    """
    
    try:
        from Commands.registry import commands
        registryCommands = commands
    except ImportError:
        print("registry.py not found.")
        exit(1)
    #Get alias from CLI
    commandalias = sys.argv[1]
    #STEP1 :  Parse command

    #STEP2 : iterate class in registry
    for alias ,commands in registryCommands.items():
        #If sys alias is in registry
        if commandalias == alias:
            CommandObject = commands()
            #If sys is help
            if '--help' in sys.argv:
                print(CommandObject.getHelp())
                exit(0)
            else:                
                result = CommandObject.execute()
                exit(result)      
    else:
        print("Failed to run any commands")



if __name__ == "__main__":
    sys.exit(main())


