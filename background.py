import pygame

class Background:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = 2001
        self.width = 2001
        self.background_box = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.background_img = pygame.image.load('./bg.jpg')
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

    def events(self):
        self.keys = pygame.key.get_pressed()
        # Each key moves the background the oposite direction that we want our character to move.
        # Scroll left
        if self.keys[pygame.K_a]:
            self.x += 20
        # Scroll right
        if self.keys[pygame.K_d]:
            self.x -= 20
        # Scroll down
        if self.keys[pygame.K_w]:
            self.y += 20
        # Scroll Up
        if self.keys[pygame.K_s]:
            self.y -= 20
        
        # get relative mouse position
        self.rel_mouse_pos = pygame.mouse.get_rel()
        # get mouse buttons
        self.mouse_buttons = pygame.mouse.get_pressed()
        # if left mouse button is pressed
        if self.mouse_buttons[0]:
            # scroll background
            self.x += self.rel_mouse_pos[0]
            self.y += self.rel_mouse_pos[1]
            
    def update(self):
        # Updatig background and border
        self.background_box = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self):
        # Drawling background and a border
        self.screen.blit(self.background_img, (self.x, self.y))
        pygame.draw.rect(self.screen, (255, 0, 0), self.background_box, 2)
