import numpy as np
from os.path import join

from matplotlib import cm

VIRIDIS = np.array(cm.get_cmap('plasma').colors)
VID_RANGE = np.linspace(0.0, 1.0, VIRIDIS.shape[0])

from PIL import Image

class Lidar(object):
    def __init__(self, sensor, args):
        self._n_frame = 0
        self._actor = sensor
        self.args = args
        self._frame = None
        self.save_path = ""

    def set_frame(self, frame):
        """Prepares a point cloud with intensity
        colors ready to be consumed by Open3D"""

        self._frame = frame

        points = np.frombuffer(frame.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0] / 4), 4))

        # Isolate the intensity and compute a color for it
        intensity = points[:, -1]
        intensity_col = 1.0 - np.log(intensity) / np.log(np.exp(-0.004 * 100))
        int_color = np.c_[
            np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 0]),
            np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 1]),
            np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 2])]
                
        lidar_range = 2.0*float(self.args.params.range)

        lidar_img_size = (self.args.lidar_img_x, self.args.lidar_img_y, 3)

        lidar_data = np.array(points[:, :2])
        lidar_data *= self.args.lidar_img_y / lidar_range
        lidar_data += (0.5 * self.args.lidar_img_x, 0.5 * self.args.lidar_img_y)
        lidar_data = np.fabs(lidar_data)  # pylint: disable=E1111
        lidar_data = lidar_data.astype(np.int32)
        lidar_data = np.reshape(lidar_data, (-1, 2))
        
        self._frame.img = np.zeros((lidar_img_size), dtype=np.uint8)
        self._frame.img[tuple(lidar_data.T)] = int_color*(255, 255, 255)

        if self.args.save:
           self.save_frame()
    
    def get_actor(self):
        return self._actor
    
    def get_frame(self):
        return self._frame
    
    def save_frame(self):
        im = Image.fromarray(self._frame.img)
        im.save(join(self.save_path, f"{self._n_frame}.jpg"))
        self._n_frame += 1