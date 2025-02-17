import sys
import importlib
import pdb
import os



#php console {program} {program_value} {--option1} {option1_value} {--option2} {option2_value} ... {--optionN} {optionN_value}

def autoload(className):
    """Autoload classes from the 'Commands' directory."""

    filePath = os.path.join(os.path.dirname(__file__), 'Commands', className.replace('\\', '/') + '.py') # Changed to camelCase
    if os.path.exists(filePath): # Changed to camelCase
        moduleName = '.'.join(['Commands', className.split('\\')[-1]]) # Changed to camelCase
        try:
            module = importlib.import_module(moduleName) # Changed to camelCase
            return getattr(module, className.split('\\')[-1]) # Changed to camelCase
        except Exception as e:
            print(f"Error loading class {className}: {e}") # Changed to camelCase
            return None
    return None

def main()->int:
    """
    Entry point of Comamnd
    Expected command----->  python console {program} {programValue} {--option1} [option1_value]  .......
    python console code-gen migration --name CreateUsersTestTable1
     
    """
    
    try:
        commands = {}
        with open("Commands/registry.php", "r") as f: # Assuming registry.php lists classes
            for line in f:
                className = line.strip() # Changed to camelCase
                if className: # Changed to camelCase
                    cls = autoload(className) # Changed to camelCase
                    if cls: # Check successful load
                        commands[cls.getAlias()] = cls

        inputCommand = sys.argv[1] if len(sys.argv) > 1 else None # Changed to camelCase

        if inputCommand: # Changed to camelCase
            if inputCommand in commands: # Changed to camelCase
                commandClass = commands[inputCommand] # Changed to camelCase
                if '--help' in sys.argv:
                    sys.stdout.write(commandClass.getHelp()) # Changed to camelCase
                    sys.exit(0)
                else:
                    command = commandClass() # Changed to camelCase
                    result = command.execute()
                    sys.exit(result)  # Exit with result code
            else:
                sys.stdout.write("Failed to run any commands\n") # Use stdout
                sys.exit(1) # Indicate failure
        else:
            sys.stdout.write("No command provided.\n") # Handle no input
            sys.exit(1) # Indicate failure

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())


