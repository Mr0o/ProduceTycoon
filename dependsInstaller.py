# Check if all the dependencies are installed
# Automatically install the missing dependencies

def isDependenciesInstalled() -> bool:
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
        print("ERROR: Failed to install dependencies using pip. \n ")
        print("Please install the dependencies manually using the command:\n ")
        print("\t{sys.executable} -m pip install -r requirements.txt \n")
        
        exit()
    



