from os.path import join
from carla import ColorConverter

class Camera(object):
    def __init__(self, sensor, args):
        self._n_frame = 0
        self._actor = sensor
        self.args = args
        self._frame = None
        self.save_path = ""

    def set_frame(self, frame):
        self._frame = frame
        if self.args.id != "rgb":
            self._frame.convert(ColorConverter.CityScapesPalette)
        if self.args.save:
            self.save_frame()
    
    def get_actor(self):
        return self._actor
    
    def get_frame(self):
        return self._frame
    
    def save_frame(self):
        self._frame.save_to_disk(join(self.save_path, self.args.id, f"{self._n_frame}.jpg"))
        self._n_frame += 1