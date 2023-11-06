# Check if all the dependencies are installed
# Automatically install the missing dependencies

def isDependenciesInstalled() -> bool:
    # first check for correct python version
    import sys

    assert not sys.version_info < (3, 10), f"""
        \x1b[31mERROR: Python {sys.version_info[0]}.{sys.version_info[1]} is not supported!\x1b[0m
        \x1b[33mPlease install Python 3.10 or higher.\x1b[0m"""
    
    # try to import dependencies
    try:
        import pygame

    except ImportError:
        return False
    
    return True


def installDependencies() -> None:
    # Try running 'python -m pip install -r requirements.txt'

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
        assert False, """
            ERROR: Failed to install dependencies using pip. \n
            Please make sure pip is installed\n"""
    
    # dependencies must be installed to continue
    assert not isDependenciesInstalled(), f"""
        ERROR: Failed to install dependencies using pip.
        Please install the dependencies manually using the command: \n
        \t{sys.executable} -m pip install -r requirements.txt \n"""
    



