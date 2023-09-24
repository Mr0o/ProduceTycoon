# Check dependencies
from dependsInstaller import isDependenciesInstalled, installDependencies
if not isDependenciesInstalled():
    installDependencies()

# Run the game
from ProduceTycoonGame.game import Game

if __name__ == '__main__':
    game = Game()
    game.run()