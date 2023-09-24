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

    # attempt installing dependencies using pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    if isDependenciesInstalled():
        return
    
    print(f"""Failed to install dependencies using pip. \n 
              Please install the dependencies manually using the command:\n 
              '\t {sys.executable} -m pip install -r requirements.txt \n""")
    



