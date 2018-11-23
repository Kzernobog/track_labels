from detection_class import Detection


class DetectionList:
    def __init__(self, bbox_list):
        self.detections_list = [Detection(bbox) for bbox in bbox_list]

    def draw(self, frame):
        """
        Returns a new frame which has bounding boxes drawn for all detections.
        :param frame: the base image frame on which boxes are drawn
        :return: a frame on which boxes are drawn
        """
        for detection in self.detections_list:
            frame = detection.draw_bbox(frame)

        return frame

    def all_marked(self):
        """
        Checks if all the detections in the detection list are marked.
        Detections are considered marked if a label has been assigned to them.
        :return: (bool) True if all marked and False otherwise
        """
        for detection in self.detections_list:
            if detection.label is None:
                return False
        return True

    def point_in_unmarked_detection_box(self, point):
        """
        Functions returns true if the given point is contained with a detection object
        which is yet unmarked.
        Returns False otherwise.
        :param point: (tuple) the point (x, y), the click coordinates
        :return: (boolean)
        """
        for detection in self.detections_list:
            if detection.point_in_box(point):
                if detection.label is not None:
                    return False
                else:
                    return True
        return False

    def get_detection_containing_point(self, point):
        """
        Given a point (x, y), return the detection object which contains the point.
        If no detection contains the point, return None
        :param point: (tuple) point (x, y), the click coordinates
        :return: (Detection) the detection containing point (else None)
        """
        for detection in self.detections_list:
            if detection.point_in_box(point):
                return detection
        return None
    def get_bbox_list(self,detections_list):

        current_detected_list = []

        for detection in detections_list:
            current_detected_list.append(detection.bbox)

        return current_detected_list

    def validate_and_update_id(self, point, label):
        """
        Given a point (x, y) which are the click coordinates and a label,
        checks if the point belongs to some detection, and if so,
        changes its id accordingly and returns True.

        If this could not be done because the label was bad or because the point
        did not belong to any detection, the detection list is unchanged and
        the functions returns False
        :param point: (tuple) (x, y) representing click coordinates
        :param label: (int) a label to identify the tank
        :return: (bool) True if update successful and False otherwise
        """
        detection_containing_point = self.get_detection_containing_point(point)

        if detection_containing_point is None:
            return False
        else:
            if type(label) is int:
                detection_containing_point.label = label
                detection_containing_point.is_marked = True
                return True
            else:
                # TODO Give an option to mark non-tank detections as null
                return False

    def reset(self):
        """
        Resets all detections to default state in the detections_list.
        All labels are removed and all detections are unmarked.
        [Use this if the user wants to reset the frame back to its original state.]
        :return: (None)
        """
        for detection in self.detections_list:
            detection.reset()

    def get_bbox_list(self):
        bbox_list = [detection.bbox for detection in self.detections_list]
        return bbox_list

    def get_labels_list(self):
        labels_list = [detection.label for detection in self.detections_list]
        return labels_list





