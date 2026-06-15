from config import SCREEN_HEIGHT, GRAVITY


class Bomb:
    def __init__(self, x, y, vx, vy, image):
        self.x = float(x)
        self.y = float(y)

        self.vx = float(vx)
        self.vy = float(vy)

        self.image = image

        self.size = image.get_width()
        self.radius = self.size // 2

        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vy += GRAVITY

        if self.y - self.radius > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        rect = self.image.get_rect(
            center=(int(self.x), int(self.y))
        )

        screen.blit(self.image, rect)