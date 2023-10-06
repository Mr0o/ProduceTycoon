# Check if all the dependencies are installed
# Automatically install the missing dependencies

def isDependenciesInstalled() -> bool:
    # first check for correct python version
    import sys
    if sys.version_info < (3, 10):
        print(f"\x1b[31mERROR: Python {sys.version_info[0]}.{sys.version_info[1]} is not supported!\x1b[0m")
        print("\n\x1b[33mPlease install Python 3.10 or higher.\x1b[0m")

        exit()
    
    # try to import dependencies
    try:
        import pygame

    except ImportError:
        return False
    
    return True


def installDependencies() -> None:
    # Try running 'pip install -r requirements.txt'
    # using variouse methods

    print("Installing dependencies... \n")

    import sys
    import subprocess
    import time

    # attempt installing dependencies using pip
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        time.sleep(1)
    except subprocess.CalledProcessError:
        # pip is likely not installed
        print("ERROR: Failed to install dependencies using pip. \n")
        print("Please make sure pip is installed\n")

        exit()
    
    # if the dependencies are still not installed
    if not isDependenciesInstalled():
        print("ERROR: Failed to install dependencies using pip.")
        print("Please install the dependencies manually using the command: \n")
        print(f"\t{sys.executable} -m pip install -r requirements.txt \n")
        
        exit()
    



