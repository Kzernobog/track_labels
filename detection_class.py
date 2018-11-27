import cv2
from typing import List

from colours import Colour


class Detection:
    def __init__(self, bbox: List[int]):
        self.bbox: List[int] = bbox  # [x_min, y_min, x_max, y_max] the detection list
        self.label: int = None  # an id to mark the detection box
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
            # TODO Provide an option for drawing black boxes for non-tank objects
            # choose a random color to draw the bbox if a color was not already picked previously
            if self.color is None:  # if the detection has not already been assigned a colour
                colour = Colour.choose_colour(self.label)
                self.color = colour
            else:
                colour = self.color

            box_thickness = 2
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), colour, box_thickness)

            # mention label on the box
            label_text = '{}'.format(self.label)
            text_colour = (255, 255, 255)
            text_size = 0.5
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
