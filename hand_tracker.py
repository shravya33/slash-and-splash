import cv2
import mediapipe as mp

from config import WEBCAM_WIDTH, WEBCAM_HEIGHT


class HandTracker:
    INDEX_FINGER_TIP = 8

    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        return frame

    def detect_hands(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb)

    def get_index_fingertip(self, frame, results):
        if not results.multi_hand_landmarks:
            return None

        h, w, _ = frame.shape

        hand = results.multi_hand_landmarks[0]
        tip = hand.landmark[self.INDEX_FINGER_TIP]

        return (
            int(tip.x * w),
            int(tip.y * h)
        )

    # def draw_landmarks(self, frame, results):
    #     if results.multi_hand_landmarks:
    #         for hand in results.multi_hand_landmarks:
    #             self.mp_drawing.draw_landmarks(
    #                 frame,
    #                 hand,
    #                 self.mp_hands.HAND_CONNECTIONS
    #             )
    #     return frame

    # def draw_fingertip(self, frame, fingertip_pos):
    #     if fingertip_pos:
    #         cv2.circle(
    #             frame,
    #             fingertip_pos,
    #             12,
    #             (0, 0, 255),
    #             -1
    #         )
    #     return frame

    def release(self):
        self.cap.release()
        self.hands.close()