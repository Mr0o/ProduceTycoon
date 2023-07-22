import pygame

from ProduceTycoonGame.vectors import Vector

class Clock():
    def __init__(self, clock: pygame.time.Clock, screen: pygame.Surface, pos: Vector):
        self.clock = clock
        self.screen = screen
        self.pos = pos

        self.font = pygame.font.SysFont('Arial', 15, bold=True)

        self.time = 0
        self.minute = 0
        self.hour = 7
        self.timeText = ""

        self.hidden = False

        self.rect = pygame.Rect(self.pos.x, self.pos.y, 100, 25)

    def events(self):
        self.time += self.clock.get_time()
        if self.time >= 6000:
            self.time = 0
            self.minute += 1
            if self.minute >= 6:
                self.minute = 0
                self.hour += 1
                if self.hour >= 13:
                    self.hour = 0

        self.timeText = self.font.render(f"{self.hour}:{self.minute}0", True, (0, 0, 0))

    def draw(self):
        if not self.hidden:
            pygame.draw.rect(self.screen, (240, 198, 60), self.rect)
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
            self.screen.blit(self.timeText, (self.pos.x + (self.rect.width/2 - self.timeText.get_width()/2), self.pos.y + (self.rect.height/2 - self.timeText.get_height()/2)))

    

