import pygame

class Tile:
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int, tile_img: pygame.Surface = pygame.image.load('./bg.jpg')):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.tile_img = tile_img

    def events(self):
        # get relative mouse position
        rel_mouse_pos = pygame.mouse.get_rel()
        # get mouse buttons
        mouse_buttons = pygame.mouse.get_pressed()
        # if left mouse button is pressed
        if mouse_buttons[0]:
            # scroll background
            self.x += rel_mouse_pos[0]
            self.y += rel_mouse_pos[1]
            
    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.tile_img, (self.x, self.y))
        print(self.x, self.y)