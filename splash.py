import pygame


class Splash:
    def __init__(self, x, y, image, color):
        self.x = x
        self.y = y

        self.life = 25
        self.max_life = 25

        self.image = image.copy()

        self.image.fill(
            color,
            special_flags=pygame.BLEND_RGBA_MULT
        )

    def update(self):
        self.life -= 1

    @property
    def active(self):
        return self.life > 0

    def draw(self, screen):
        alpha = int(
            255 * (self.life / self.max_life)
        )

        splash = self.image.copy()

        splash.set_alpha(alpha)

        rect = splash.get_rect(
            center=(int(self.x), int(self.y))
        )

        screen.blit(splash, rect)