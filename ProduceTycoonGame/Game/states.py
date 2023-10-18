from abc import ABC, abstractmethod
import pygame

class State(ABC):

    @property
    def getGame(self):
        return self.game

    @gameState.setter
    def setGame(self, game: Game):
        self.game = game

    @abstractmethod
    def events(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass



    
