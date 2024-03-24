from collections.abc import Callable, Iterable, Mapping
from typing import Any
import cv2
import autopy
import mediapipe as mp
import time
import asyncio
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from threading import Thread, Event


class MouseControl:
    
    def __init__(self, event: Event):
        self.enable = event
    
    def run(self): 
        cap = cv2.VideoCapture(0)
        WIDTH, HEIGHT = autopy.screen.size()

        hands = mp.solutions.hands.Hands(static_image_mode=False,
                                        max_num_hands=1,
                                        min_tracking_confidence=0.5,
                                        min_detection_confidence=0.5)

        mpDraw = mp.solutions.drawing_utils

        click_state = False
        while not self.enable.is_set():
            _, res = cap.read()
            img = cv2.flip(res, 1)
            result = hands.process(img)
            cx_4 = cy_4 = cx_5 = cy_5 = None
            if result.multi_hand_landmarks:
                for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255))
                    if id == 8:
                        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                        try:
                            autopy.mouse.move(cx * WIDTH / w, cy * HEIGHT / h)
                        except:
                            pass
                    if id == 4:
                        cx_4, cy_4 = cx, cy
                        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                    if id == 5:
                        cx_5, cy_5 = cx, cy
                        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                    if cx_4 and cx_5:
                        if abs(cx_4 - cx_5) < 30 and abs(cy_4 - cy_5) < 30:
                            if not click_state: 
                                # print("click")
                                autopy.mouse.click()
                                click_state = True
                        else:
                            if click_state:
                                # print("unclick")
                                click_state = False
                # mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)
            # print(result)
            # cv2.imshow("123", img)
            # cv2.waitKey(1)


class MouseThread(Thread):
    
    def __init__(self):
        super().__init__()
        self.need_term = Event()

    def run(self):
        self.mouse_control = MouseControl(self.need_term)
        self.mouse_control.run()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    WIDTH, HEIGHT = autopy.screen.size()

    hands = mp.solutions.hands.Hands(static_image_mode=False,
                                    max_num_hands=1,
                                    min_tracking_confidence=0.5,
                                    min_detection_confidence=0.5)

    mpDraw = mp.solutions.drawing_utils

    click_state = False
    while True:
        _, res = cap.read()
        img = cv2.flip(res, 1)
        result = hands.process(img)
        cx_4 = cy_4 = cx_5 = cy_5 = None
        if result.multi_hand_landmarks:
            for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv2.circle(img, (cx, cy), 3, (255, 0, 255))
                if id == 8:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                    try:
                        autopy.mouse.move(cx * WIDTH / w, cy * HEIGHT / h)
                    except:
                        pass
                if id == 4:
                    cx_4, cy_4 = cx, cy
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                if id == 5:
                    cx_5, cy_5 = cx, cy
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
                if cx_4 and cx_5:
                    if abs(cx_4 - cx_5) < 30 and abs(cy_4 - cy_5) < 30:
                        cv2.circle(img, (cx_4, cy_4), 10, (0, 255, 0), cv2.FILLED)
                        cv2.circle(img, (cx_5, cy_5), 10, (0, 255, 0), cv2.FILLED)
                        if not click_state: 
                            print("click")
                            autopy.mouse.click()
                            click_state = True
                    else:
                        if click_state:
                            print("unclick")
                            autopy.mouse.click()
                            click_state = False
            # mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)
        # print(result)
        cv2.imshow("123", img)
        cv2.waitKey(1)