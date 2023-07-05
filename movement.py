import pygame

class Movement:
    @classmethod
    def check_if_move(cls, x: int, y: int):
        keys = pygame.key.get_pressed()
        # Each key moves the background the oposite direction that we want our character to move.
        # Scroll left
        if keys[pygame.K_a]:
            x += 20
        # Scroll right
        if keys[pygame.K_d]:
            x -= 20
        # Scroll down
        if keys[pygame.K_w]:
            y += 20
        # Scroll Up
        if keys[pygame.K_s]:
            y -= 20
        
        # get relative mouse position
        rel_mouse_pos = pygame.mouse.get_rel()
        # get mouse buttons
        mouse_buttons = pygame.mouse.get_pressed()
        # if left mouse button is pressed
        if mouse_buttons[0]:
            # scroll background
            x += rel_mouse_pos[0]
            y += rel_mouse_pos[1]
        return (x, y)
