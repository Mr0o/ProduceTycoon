"""Author: Owen Smith (Mr0)
\n Simple message box module
\n Only one instance of MessageBox needs to be created
\n When a message is posted to the message box, it will be displayed in the center of the screen
\n The message str can be split by newlines
\n The message box does not do anything else beyond displaying a message with an OK button
\n Intended for basic output to the player
"""

import pygame

from ProduceTycoonGame.events import eventOccured, getEvent
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import ButtonInfo, Button

class MessageBox:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.message = ""

        self.font = pygame.font.SysFont('Arial', 20, bold=True)
        self.text = self.font.render(self.message, True, (0, 0, 0))

        # message box rect
        self.rect = pygame.Rect((self.screen.get_width()/2 - 200, self.screen.get_height()/2 - 100), (400, 200))
        # outline of message box
        self.outline = pygame.Rect((self.rect.x - 2, self.rect.y - 2), (self.rect.width + 4, self.rect.height + 4))
        # button positioned at bottom right of message box
        self.button = Button(Vector(self.rect.x + self.rect.width - 105, self.rect.y + self.rect.height - 55), "OK", 100, 50, lambda: self.dismiss())

        self.dismissed = True

    def postMessage(self, message: str) -> None:
        # activate the messageBox and render the message text
        self.message = message
        self.dismissed = False

    def events(self) -> None:
        # check if any message post events have occured
        if eventOccured("postMessage") and self.dismissed:
            # get the message event
            messageEvent = getEvent("postMessage")

            # post the message to the message box
            self.postMessage(str(messageEvent.eventData))

        # check if the window has been resized
        if eventOccured("windowResize"):
            # update the message box rects and button position
            self.updatePos()

        self.button.events()

    def dismiss(self):
        self.dismissed = True

    def updatePos(self) -> None:
        self.rect = pygame.Rect((self.screen.get_width()/2 - 200, self.screen.get_height()/2 - 100), (400, 200))
        self.outline = pygame.Rect((self.rect.x - 2, self.rect.y - 2), (self.rect.width + 4, self.rect.height + 4))
        self.button.setPos(Vector(self.rect.x + self.rect.width - 105, self.rect.y + self.rect.height - 55))
        
    def draw(self) -> None:
        if not self.dismissed:
            pygame.draw.rect(self.screen, (0, 0, 0), self.outline)
            pygame.draw.rect(self.screen, (110, 190, 210), self.rect)

            self.button.draw()
            
            # split message into message lines
            lines = self.message.split("\n")
            # render each message line
            for i in range(len(lines)):
                self.text = self.font.render(lines[i], True, (0, 0, 0))
                ## draw message line
                self.screen.blit(self.text, (self.screen.get_width()/2 - self.text.get_width()/2, self.screen.get_height()/2 - self.text.get_height()/2 - 25 + i * 25))
