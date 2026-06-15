import pygame
import random
import cv2
import os

from fruit import Fruit
from collision import swipe_hits_fruit
from config import *
from splash import Splash
from bomb import Bomb


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.state = STATE_MENU

        pygame.display.set_caption(WINDOW_TITLE)

        self.menu_background = pygame.image.load("assets/ui/menu_background.png").convert()
        self.menu_background = pygame.transform.scale(self.menu_background,(SCREEN_WIDTH, SCREEN_HEIGHT))

        self.heart_image = pygame.image.load("assets/ui/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image,(32, 32))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf",18)
        self.big_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf",36)

        self.running = True
        self.game_over = False

        self.fruits = []
        self.spawn_timer = 0

        self.score = 0
        self.lives = 3

        self.high_score = self.load_high_score()

        self.fruit_images = self.load_fruit_assets()

        self.bomb_image = pygame.image.load("assets/bombs/bomb.png").convert_alpha()
        self.bomb_image = pygame.transform.scale(self.bomb_image,(BOMB_SIZE, BOMB_SIZE))

        self.splashes=[]
        self.splash_image = pygame.image.load("assets/effects/splash.png").convert_alpha()
        self.splash_image = pygame.transform.scale(self.splash_image,(140, 140))

        self.bombs=[]
        self.explosion_image = pygame.image.load("assets/effects/explosion.png").convert_alpha()
        self.explosion_image = pygame.transform.scale(self.explosion_image,(180, 180))

    def draw_lives(self):
        start_x = 20
        y = 10

        for i in range(self.lives):
            self.screen.blit(self.heart_image,(start_x + (i * 35), y))

    def load_fruit_assets(self):
        fruit_images = {}

        for filename in FRUIT_FILES:
            path = os.path.join("assets","fruits",filename)

            if os.path.exists(path):
                fruit_name = filename.replace(".png","")
                size = FRUIT_SIZES.get(fruit_name,90)
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image,(size, size))
                fruit_images[fruit_name] = image
                
        if not fruit_images:
            raise RuntimeError("No fruit PNG assets found in assets/fruits/")

        return fruit_images

    def spawn_fruit(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = SCREEN_HEIGHT + 50

        vx = random.uniform(MIN_VX, MAX_VX)
        vy = random.uniform(MIN_VY, MAX_VY)

        fruit_name, image = random.choice(list(self.fruit_images.items()))

        self.fruits.append(
        Fruit(
            x,
            y,
            vx,
            vy,
            image,
            fruit_name
        )
    )

    def spawn_bomb(self):
        x = random.randint(100,SCREEN_WIDTH - 100)
        y = SCREEN_HEIGHT + 50
        vx = random.uniform(MIN_VX,MAX_VX)
        vy = random.uniform(MIN_VY,MAX_VY)

        self.bombs.append(Bomb(x,y,vx,vy, self.bomb_image))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.return_to_menu()

    def restart(self):
        self.fruits.clear()
        self.spawn_timer = 0
        self.score = 0
        self.lives = 3
        self.game_over = False

    def start_game(self):
        self.fruits.clear()
        self.bombs.clear()
        self.splashes.clear()

        self.score = 0
        self.lives = 3

        self.game_over = False
        self.state = STATE_PLAYING

    def return_to_menu(self):
        self.state = STATE_MENU

    def load_high_score(self):
        try:
            with open("highscore.txt","r") as file:
                return int(file.read().strip())
        except:
            return 0

    def save_high_score(self):
        with open("highscore.txt","w") as file:
            file.write(str(self.high_score))

    def handle_collisions(self, swipe_line, is_swiping):
        if not is_swiping:
            return

        if swipe_line is None:
            return

        for fruit in self.fruits:
            if fruit.active and swipe_hits_fruit(
                swipe_line,
                fruit
            ):
                fruit.active = False
                fruit.sliced = True
                color = FRUIT_COLORS.get(fruit.fruit_name,(255, 255, 255))
                self.splashes.append(Splash(fruit.x,fruit.y,self.splash_image,color))
                self.score += 1

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()

        for bomb in self.bombs:
            if bomb.active and swipe_hits_fruit(swipe_line,bomb):
                bomb.active = False
                self.splashes.append(Splash(bomb.x,bomb.y,self.explosion_image,EXPLOSION_COLOR))
                self.game_over = True
                self.state = STATE_GAME_OVER

    def handle_missed_fruits(self):
        for fruit in self.fruits:
            if not fruit.active and not fruit.sliced:
                self.lives -= 1

        if self.lives <= 0:
            self.game_over = True
            self.state = STATE_GAME_OVER

    def update(self, swipe_line=None, is_swiping=False):
        if self.state != STATE_PLAYING:
            return

        self.spawn_timer += 1

        if self.spawn_timer >= SPAWN_INTERVAL:
            if random.random() < BOMB_SPAWN_CHANCE:
                self.spawn_bomb()
            else:
                self.spawn_fruit()

            self.spawn_timer = 0

        self.handle_collisions(
            swipe_line,
            is_swiping
        )

        for fruit in self.fruits:
            fruit.update()

        for bomb in self.bombs:
            bomb.update()

        self.handle_missed_fruits()

        self.fruits = [
            fruit for fruit in self.fruits
            if fruit.active
        ]

        for splash in self.splashes:
            splash.update()

        self.splashes = [
        splash
        for splash in self.splashes
            if splash.active
        ]

        self.bombs = [
            bomb
            for bomb in self.bombs
            if bomb.active
        ]

    def convert_frame_to_surface(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rgb = cv2.resize(
            rgb,
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        rgb = rgb.swapaxes(0, 1)

        return pygame.surfarray.make_surface(rgb)

    def render(self, frame, is_swiping, gesture):
        if self.state == STATE_MENU:
            self.render_menu()
            return

        if self.state == STATE_GAME_OVER:
            self.render_game_over()
            return
        webcam_surface = self.convert_frame_to_surface(frame)

        self.screen.blit(webcam_surface, (0, 0))

        for splash in self.splashes:
            splash.draw(self.screen)

        for bomb in self.bombs:
            bomb.draw(self.screen)

        for fruit in self.fruits:
            fruit.draw(self.screen)

        gesture.draw_game_trail(self.screen)

        self.draw_header()
        
        score = self.font.render(
            f"Score: {self.score}",
            True,
            (255,255,255)
        )

        score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 25))

        high_score = self.font.render(
            f"High Score: {self.high_score}",
            True,
            (255,255,0)
        )

        best_rect = high_score.get_rect(midright=(SCREEN_WIDTH - 20,25))

        self.screen.blit(score, score_rect)
        self.screen.blit(high_score, best_rect)
        self.draw_lives()

        if self.game_over:
            over = self.big_font.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            restart = self.font.render(
                "Press R to Restart",
                True,
                TEXT_COLOR
            )

            final_score = self.font.render(f"Score: {self.score}",True,TEXT_COLOR)
            best_score = self.font.render(f"High Score: {self.high_score}",True,TEXT_COLOR)

            self.screen.blit(over, (280, 280))
            self.screen.blit(restart, (360, 380))
            self.screen.blit(final_score, (390, 450))
            self.screen.blit(best_score, (360, 500))

        pygame.display.flip()

    def draw_header(self):
        header = pygame.Surface((SCREEN_WIDTH, 50),pygame.SRCALPHA)
        header.fill((0, 0, 0, 120))

        self.screen.blit(header,(0, 0))

    def render_menu(self):
        self.screen.blit(self.menu_background,(0, 0))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("SLASH & SPLASH",True, (255, 255, 255))

        start = self.font.render("SPACE - START",True,(255, 255, 255))

        quit_text = self.font.render("ESC - QUIT",True,(255, 255, 255))

        high_score = self.font.render(f"BEST: {self.high_score}",True,(255, 0, 0))

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 180))
        highscore_rect = high_score.get_rect(center=(SCREEN_WIDTH // 2, 300))
        start_rect = start.get_rect(center=(SCREEN_WIDTH // 2, 400))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, 450))

        self.screen.blit(title,title_rect)
        self.screen.blit(high_score, highscore_rect)
        self.screen.blit(start, start_rect)
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

    def render_game_over(self):
        self.screen.blit(self.menu_background,(0, 0))
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        over = self.big_font.render("GAME OVER",True,(255, 60, 60))

        score = self.font.render(f"SCORE {self.score}",True,(255, 255, 255))

        best = self.font.render(f"BEST {self.high_score}",True,(255, 255, 0))

        restart = self.font.render("R - MENU",True,(255, 255, 255))

        over_rect = over.get_rect(center=(SCREEN_WIDTH // 2, 220))
        score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 330))
        best_rect = best.get_rect(center=(SCREEN_WIDTH // 2, 380))
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, 470))

        self.screen.blit(over, over_rect)
        self.screen.blit(score, score_rect)
        self.screen.blit(best, best_rect)
        self.screen.blit(restart, restart_rect)

        pygame.display.flip()

    def tick(self):
        self.clock.tick(FPS)

    def cleanup(self):
        pygame.quit()