import cv2
from typing import List


class Detection:
    def __init__(self, bbox: List[int]):
        self.bbox = bbox  # [x_min, y_min, x_max, y_max] the detection list
        self.label = None  # an id to mark the detection box
        self.is_marked = False  # true if box is labelled and false otherwise

    def draw_bbox(self, frame):
        frame = frame.copy()
        x_min, y_min, x_max, y_max = self.bbox

        if self.label is None:
            # draw a thin white box
            colour = (255, 255, 255)
            box_thickness = 1
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), colour, box_thickness)

        else:
            # TODO Provide an option for drawing black boxes for non-tank objects
            # draw a slightly thicker red box
            # TODO use different colours for each box (perhaps choosing them randomly)
            colour = (0, 0, 255)
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
        self.is_marked = False
