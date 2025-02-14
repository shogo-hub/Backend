import sys
import importlib
import pdb




#php console {program} {program_value} {--option1} {option1_value} {--option2} {option2_value} ... {--optionN} {optionN_value}

def autoload(class_name):
    """クラスを自動で読み込む"""
    try:
        module_name = '.'.join(class_name.split('.')[:-1])
        class_name = class_name.split('.')[-1]
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, AttributeError):
        return None

def main()->int:
    """
    Entry point of Comamnd
    Expected command----->  python console {program} {programValue} {--option1} [option1_value]  .......
    python console code-gen migration --name CreateUsersTestTable1
     
    """
    #pdb.set_trace()

    #STEP 1: Parse command
    if len(sys.argv) < 2:
        print("Usage: python console.py <command> [--help]", file=sys.stderr)
        return 1
    inputCommand = sys.argv[1]

    #STEP 2 : Import code to run
    try:
        from .Commands.registry import commands
    except ImportError:
        print("Failed to load commands registry.", file=sys.stderr)
        return 1
    
    #STEP 3 : Execute class
    if inputCommand in commands:
        commandClass = commands[inputCommand]
        if '--help' in sys.argv:
            print(commandClass.get_help())
            return 0
        else:
            command = commandClass()
            result = command.execute()
            return result
    else:
        print("Failed to run any commands.", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())


