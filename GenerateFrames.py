import cv2
import numpy as np
from CartoonFrames import cartoon

class GenerateFrames:

    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        success, self.next_frame = self.camera.read()
        if not success:
            self.camera.release()
            self.camera = cv2.VideoCapture(1)

        self.frame_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fov_coordinates = [[0, 0], [self.frame_width, 0], [0, self.frame_height], [self.frame_width, self.frame_height]]

    def _raw_video_generator(self):
        while True:
            ret_value, next_frame = self.camera.read()

            ret_value, frame_as_jpeg = cv2.imencode(".jpg", next_frame)
            next_frame = frame_as_jpeg.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + next_frame + b"\r\n\r\n")

    def _cartoon_video_generator(self):
        while True:
            ret_value, next_frame = self.camera.read()
            cartoon_frame = cartoon(next_frame)

            ret_value, frame_as_jpeg = cv2.imencode(".jpg", cartoon_frame)
            next_frame = frame_as_jpeg.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + next_frame + b"\r\n\r\n")

    def generate_frame(self, video_type):
        if video_type == "RawVideo":
            return self._raw_video_generator()
        elif video_type == "Cartoon":
            return self._cartoon_video_generator()