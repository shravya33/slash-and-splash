# test_setup.py

import cv2
import mediapipe as mp
import pygame
import numpy as np

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WEBCAM_WIDTH,
    WEBCAM_HEIGHT,
    WINDOW_TITLE
)


def test_imports():
    print("Testing imports...")
    print("OpenCV:", cv2.__version__)
    print("MediaPipe:", mp.__version__)
    print("Pygame:", pygame.version.ver)
    print("NumPy:", np.__version__)
    print("Imports successful.\n")


def test_pygame_window():
    print("Testing Pygame window...")

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    running = True
    frame_count = 0

    while running and frame_count < FPS * 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        pygame.display.flip()

        clock.tick(FPS)
        frame_count += 1

    pygame.quit()

    print("Pygame window test successful.\n")


def test_webcam():
    print("Testing webcam...")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Webcam could not be opened.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)

    print("Press Q to close webcam test.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Could not read webcam frame.")
            break

        frame = cv2.flip(frame, 1)

        cv2.putText(
            frame,
            "Webcam Test - Press Q to Exit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Webcam Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("Webcam test successful.\n")


if __name__ == "__main__":
    test_imports()
    test_pygame_window()
    test_webcam()

    print("PHASE 1 SETUP COMPLETE.")