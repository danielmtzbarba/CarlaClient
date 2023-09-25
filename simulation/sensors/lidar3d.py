import numpy as np
from os.path import join

from matplotlib import cm

VIRIDIS = np.array(cm.get_cmap('plasma').colors)
VID_RANGE = np.linspace(0.0, 1.0, VIRIDIS.shape[0])

import open3d as o3d

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
        data = np.copy(np.frombuffer(frame.raw_data, dtype=np.dtype('f4')))
        data = np.reshape(data, (int(data.shape[0] / 4), 4))

        # Isolate the intensity and compute a color for it
        intensity = data[:, -1]
        intensity_col = 1.0 - np.log(intensity) / np.log(np.exp(-0.004 * 100))
        int_color = np.c_[
            np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 0]),
            np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 1]),
            np.interp(intensity_col, VID_RANGE, VIRIDIS[:, 2])]

        # Isolate the 3D data
        points = data[:, :-1]

        # We're negating the y to correclty visualize a world that matches
        # what we see in Unreal since Open3D uses a right-handed coordinate system
        points[:, :1] = -points[:, :1]

        # # An example of converting points from sensor to vehicle space if we had
        # # a carla.Transform variable named "tran":
        # points = np.append(points, np.ones((points.shape[0], 1)), axis=1)
        # points = np.dot(tran.get_matrix(), points.T).T
        # points = points[:, :-1]

        point_list.points = o3d.utility.Vector3dVector(points)
        point_list.colors = o3d.utility.Vector3dVector(int_color)

       # self._frame = frame
        if self.args.save:
            self.save_frame()
    
    def get_actor(self):
        return self._actor
    
    def get_frame(self):
        return self._frame
    
    def save_frame(self):
        self._frame.save_to_disk(join(self.save_path, self.args.id, f"{self._n_frame}.jpg"))
        self._n_frame += 1