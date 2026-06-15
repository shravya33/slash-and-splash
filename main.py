from hand_tracker import HandTracker
from gesture import GestureDetector
from game import Game
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WEBCAM_WIDTH,
    WEBCAM_HEIGHT
)


def map_to_game_coords(point):
    if point is None:
        return None

    x, y = point

    mapped_x = int(
        x * SCREEN_WIDTH / WEBCAM_WIDTH
    )

    mapped_y = int(
        y * SCREEN_HEIGHT / WEBCAM_HEIGHT
    )

    return (mapped_x, mapped_y)


def main():
    tracker = HandTracker()
    gesture = GestureDetector()
    game = Game()

    try:
        while game.running:
            game.process_events()

            frame = tracker.get_frame()

            if frame is None:
                break

            results = tracker.detect_hands(frame)

            fingertip = tracker.get_index_fingertip(
                frame,
                results
            )

            game_fingertip = map_to_game_coords(
                fingertip
            )

            is_swiping = gesture.update(
                game_fingertip
            )

            swipe_line = gesture.get_swipe_line()

            # frame = tracker.draw_landmarks(
            #     frame,
            #     results
            # )

            # frame = tracker.draw_fingertip(
            #     frame,
            #     fingertip
            # )

            # frame = gesture.draw_swipe_status(
            #     frame,
            #     is_swiping
            # )

            game.update(
                swipe_line=swipe_line,
                is_swiping=is_swiping
            )

            game.render(frame, is_swiping, gesture)
            game.tick()

    finally:
        tracker.release()
        game.cleanup()


if __name__ == "__main__":
    main()