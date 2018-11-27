import cv2
from typing import List

from colours import Colour


class Detection:
    def __init__(self, bbox: List[int]):
        self.bbox: List[int] = bbox  # [x_min, y_min, x_max, y_max] the detection list
        self.label: int = None  # an id to mark the detection box (-1 for no-tank, -2 for occlusion)
        self.color = None

    def draw_bbox(self, frame):
        frame = frame.copy()
        x_min, y_min, x_max, y_max = self.bbox

        if self.label is None: # if the tank is not marked yet
            # draw a thin white box
            colour = (255, 255, 255)
            box_thickness = 1
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), colour, box_thickness)

        else:  # if the tank is marked
            if self.label == -1:  # no tank
                label_text = 'Not Tank'
                colour = (0, 0, 0)
                box_thickness = 1
                text_size = 0.5

            elif self.label == -2:  # tank on tank occlusion
                label_text = 'T-T Occ'
                colour = (0, 0, 255)
                box_thickness = 3
                text_size = 0.5

            else:  # the label is positive, meaning it is a proper tank
                label_text = 'ID: {}'.format(self.label)
                colour = Colour.choose_colour(self.label)
                box_thickness = 2
                text_size = 0.5

            text_colour = (255, 255, 255)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), colour, box_thickness)
            cv2.putText(frame, label_text, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, text_size,
                        text_colour, 1, cv2.LINE_AA)

        return frame

    def point_in_box(self, point):
        """ returns the clicked region of interest
        params: point - a tuple consisting of the mouse event pixel coordinate
        return: True/False - a boolean"""
        (x, y) = point
        x_min, y_min, x_max, y_max = self.bbox
        if x_min < x < x_max and y_min < y < y_max:
            return True
        else:
            return False

    def reset(self):
        self.label = None
        self.color = None
