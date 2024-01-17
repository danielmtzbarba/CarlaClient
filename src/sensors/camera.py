import numpy as np
from os.path import join

from matplotlib import cm
from carla import ColorConverter

convs = {
    "sem": ColorConverter.CityScapesPalette,
    "bev": ColorConverter.CityScapesPalette,
    "rgbd": ColorConverter.Depth,
    "rgb": ColorConverter.Raw,
}

class Camera(object):
    def __init__(self, sensor, args):
        self._n_frame = 0
        self._actor = sensor
        self.args = args
        self._frame = None
        self.save_path = ""

    def set_frame(self, frame):
        self._frame = frame
        conv = convs[self.args.id]
        self._frame.convert(conv)

        if self.args.save:
            self.save_frame()
    
    def get_actor(self):
        return self._actor
    
    def get_frame(self):
        return self._frame
    
    def save_frame(self):
        im_path = join(self.save_path,
                    f"{self._n_frame}.jpg")
        
        self._frame.save_to_disk(im_path)
        self._n_frame += 1