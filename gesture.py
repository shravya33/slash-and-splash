# gesture.py

import math
import cv2
import pygame

from config import SWIPE_THRESHOLD, TRAIL_LENGTH


class GestureDetector:
    """
    Detects swipe gestures from fingertip motion.
    """

    def __init__(self):
        self.positions = []

    def update(self, fingertip_pos):
        """
        Update movement history.
        """
        if fingertip_pos is None:
            self.positions.clear()
            return False

        self.positions.append(fingertip_pos)

        if len(self.positions) > TRAIL_LENGTH:
            self.positions.pop(0)

        return self.is_swiping()

    def is_swiping(self):
        """
        Determine if motion exceeds threshold.
        """
        if len(self.positions) < 2:
            return False

        x1, y1 = self.positions[-2]
        x2, y2 = self.positions[-1]

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance > SWIPE_THRESHOLD

    # def draw_trail(self, frame):
    #     if len(self.positions) < 2:
    #         return frame

    #     total = len(self.positions)

    #     for i in range(1, total):
    #         start = self.positions[i - 1]
    #         end = self.positions[i]

    #         thickness = max(1, int(i * 1.8))

    #         cv2.line(
    #             frame,
    #             start,
    #             end,
    #             (0, 255, 255),
    #             thickness
    #         )

    #     return frame

    # def draw_swipe_status(self, frame, is_swiping):
    #     """
    #     Show swipe state.
    #     """
    #     text = "SWIPING" if is_swiping else "IDLE"

    #     color = (0, 0, 255) if is_swiping else (0, 255, 0)

    #     cv2.putText(
    #         frame,
    #         text,
    #         (20, 80),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         1,
    #         color,
    #         2
    #     )

    #     return frame

    def get_swipe_line(self):
        """
        Return latest swipe segment.
        Used later for collision detection.
        """
        if len(self.positions) < 2:
            return None

        return (self.positions[-2], self.positions[-1])

    
    def draw_game_trail(self, screen):
        if len(self.positions) < 2:
            return

        total = len(self.positions)

        for i in range(1, total):
            start = self.positions[i - 1]
            end = self.positions[i]

            thickness = max(2, i)

            pygame.draw.line(
                screen,
                (0, 255, 255),
                start,
                end,
                thickness
            )
