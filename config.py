# config.py

SCREEN_WIDTH = 960 #1280
SCREEN_HEIGHT = 720
FPS = 60

WEBCAM_WIDTH = 640
WEBCAM_HEIGHT = 480

WINDOW_TITLE = "Gesture Fruit Ninja MVP"

SWIPE_THRESHOLD = 28
TRAIL_LENGTH = 15

BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = (255, 255, 255)

STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

FRUIT_SIZES = {
    "apple": 90,
    "orange": 90,
    "banana": 120,
    "watermelon": 150
}

GRAVITY = 0.6

SPAWN_INTERVAL = 45

MIN_VX = -4
MAX_VX = 4

MIN_VY = -32
MAX_VY = -20

FRUIT_FILES = [
    "apple.png",
    "banana.png",
    "orange.png",
    "watermelon.png"
]

FRUIT_COLORS = {
    "apple": (255, 60, 60),
    "banana": (255, 255, 80),
    "orange": (255, 165, 0),
    "watermelon": (255, 100, 100)
}

BOMB_SIZE = 100

BOMB_SPAWN_CHANCE = 0.15

EXPLOSION_COLOR = (255,220,50)