import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type

class Button():
    def __init__(self, screen: pygame.Surface, pos: Vector,tileMap: TileMap, text = "3x3"):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap
        self.text = text

        self.width = 21
        self.height = 20
        self.color = (0, 0, 255)
        self.showRect = False
        self.posInteractable = Vector(0, 0)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        self.interactableRect = pygame.Rect(0, 0, self.screen.get_height() // 25 * 3, self.screen.get_height() // 25 * 3)
    
    def events(self, mouseClicked: bool, zeroClicked: bool):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and mouseClicked:
            self.color = (0, 123, 255)
            self.showRect = True
        else:
            self.color = (0, 0, 255)

        if self.showRect:
            for tile in self.tileMap.tileMapGrid:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    self.posInteractable.x = tile.pos.x + tile.size / 2 
                    self.posInteractable.y = tile.pos.y + tile.size / 2
                    if self.interactableRect.colliderect(tile.rect):
                        tile.type = Type.INTERACTABLE
                        self.tileMap.staticSurface = createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
        if zeroClicked:
            self.showRect = False
        


    def update(self):
        self.interactableRect.center = (self.posInteractable.x, self.posInteractable.y)
        createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
        

    def draw(self):
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(text, (self.pos.x, self.pos.y))

        if self.showRect:
            pygame.draw.rect(self.screen, self.color, self.interactableRect)