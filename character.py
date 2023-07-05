import pygame

class Character:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 20
        self.height = 45
        self.animation_images = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (120, 120, 120)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

        self.background_x = -1000
        self.background_y = -1000
        self.display_scroll = [0, 0]
        self.background_height = 2001
        self.background_width = 2001
        self.background_box = pygame.Rect((self.background_x, self.background_y), (self.background_width, self.background_height))

    def events(self):
        if (self.animation_count >= 15):
            self.animation_count = 0
        self.animation_count += 1

        self.keys = pygame.key.get_pressed()
        # Each key moves the background the oposite direction as we want our character to move.
        # Scroll left
        if self.keys[pygame.K_a]:
            self.display_scroll[0] -= 20
            self.x -= 20
        # Scroll right
        if self.keys[pygame.K_d]:
            self.display_scroll[0] += 20
            self.x += 20
        # Scroll down
        if self.keys[pygame.K_w]:
            self.display_scroll[1] -= 20
            self.y -= 20
        # Scroll Up
        if self.keys[pygame.K_s]:
            self.display_scroll[1] += 20
            self.y += 20

        # get relative mouse position
        self.rel_mouse_pos = pygame.mouse.get_rel()
        # get mouse buttons
        self.mouse_buttons = pygame.mouse.get_pressed()
        # if left mouse button is pressed
        if self.mouse_buttons[0]:
            # scroll background
            self.display_scroll[0] -= self.rel_mouse_pos[0]
            self.display_scroll[1] -= self.rel_mouse_pos[1]


    def update(self):
        # redrawling background image and border
        self.background_box = pygame.Rect((self.background_x - self.display_scroll[0], self.background_y - self.display_scroll[1]), (self.background_width, self.background_height))

        # updating character position
        self.rect = pygame.Rect((self.x - self.display_scroll[0], self.y - self.display_scroll[1]), (self.width, self.height))


    def draw(self):
        # Creating a background and a border
        pygame.draw.rect(self.screen, (0, 255, 0), self.background_box)
        pygame.draw.rect(self.screen, (255, 0, 0), self.background_box, 2)

        #pygame.draw.rect(self.screen, self.animation_images[self.animation_count//4][0], pygame.transform.scale((self.character_rect), (self.width * self.animation_images[self.animation_count//4][1], self.height * self.animation_images[self.animation_count//4][1])))
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//4], self.rect)