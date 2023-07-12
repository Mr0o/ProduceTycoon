import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type

class ObjectButton(Button):
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, text: str):
        super().__init__(screen, pos, text, False)
        self.tileMap = tileMap
        
        self.posInteractable = Vector(0, 0)
        self.showRect = False
        self.interactableRect = pygame.Rect(0, 0, self.screen.get_height() // 25 * 3, self.screen.get_height() // 25 * 3)
    
    def events(self, mouseClicked: bool):
        if self.showRect:
            for tile in self.tileMap.tileMapGrid:
                # changes center of interactable object to center of current tile
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    self.posInteractable.x = tile.pos.x + tile.size / 2 
                    self.posInteractable.y = tile.pos.y + tile.size / 2
                # changes tile type to interactable if interactableRect collides with tile and mouse is clicked
                if self.interactableRect.colliderect(tile.rect) and mouseClicked and not(self.rect.collidepoint(pygame.mouse.get_pos())):
                    tile.type = Type.INTERACTABLE
                    self.tileMap.staticSurface = createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
                    pygame.draw.rect(self.screen, self.color, self.interactableRect)
                    self.showRect = False
        super().events(mouseClicked)

    def update(self):
        super().update()
        self.interactableRect.center = (self.posInteractable.x, self.posInteractable.y)
        createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)

    def draw(self):
        if self.showRect:
            pygame.draw.rect(self.screen, self.color, self.interactableRect)

        super().draw()
