#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import carla
import pygame
from PIL import Image
import cv2

import numpy as np

from scipy.spatial.transform import Rotation as R

from utils.utils import Timer

SAVE_EVERY = 3

class SensorManager:
    def __init__(self, world, display_man, sensor_type,
                  transform, attached, sensor_options, display_pos,
                  save_dir, render_enabled = True):
        
        self.surface = None
        self.world = world
        self.display_man = display_man
        self.display_pos = display_pos
        self.render_enabled = render_enabled
        self.rgb_camera = None
        self.sensor = self.init_sensor(sensor_type, transform, attached, sensor_options)
        self.sensor_options = sensor_options
        self.vehicle = attached
        self.timer = Timer()

        self.time_processing = 0.0
        self.tics_processing = 0
        self.frames_saved = 0

        self.display_man.add_sensor(self)

        self.save_dir = save_dir

    def init_sensor(self, sensor_type, transform, attached, sensor_options):
        if sensor_type == 'RGBCamera':
            camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
            disp_size = self.display_man.get_display_size()
            camera_bp.set_attribute('image_size_x', str(disp_size[0]))
            camera_bp.set_attribute('image_size_y', str(disp_size[1]))

            for key in sensor_options:
                camera_bp.set_attribute(key, sensor_options[key])
            camera = self.world.spawn_actor(camera_bp, transform, attach_to=attached)
            camera.listen(self.save_rgb_image)
            self.rgb_camera = camera
            return camera
        
        if sensor_type == 'SemCamera':
            sem_camera_bp = self.world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
            disp_size = self.display_man.get_display_size()
            sem_camera_bp.set_attribute('image_size_x', str(disp_size[0]))
            sem_camera_bp.set_attribute('image_size_y', str(disp_size[1]))
            sem_camera_bp.set_attribute('fov', str(90.0))


            for key in sensor_options:
                sem_camera_bp.set_attribute(key, sensor_options[key])

            sem_camera = self.world.spawn_actor(sem_camera_bp, transform, attach_to=attached)
            sem_camera.listen(self.save_sem_camera)

            return sem_camera

        elif sensor_type == 'LiDAR':
            lidar_bp = self.world.get_blueprint_library().find('sensor.lidar.ray_cast')
            lidar_bp.set_attribute('dropoff_general_rate', lidar_bp.get_attribute('dropoff_general_rate').recommended_values[0])
            lidar_bp.set_attribute('dropoff_intensity_limit', lidar_bp.get_attribute('dropoff_intensity_limit').recommended_values[0])
            lidar_bp.set_attribute('dropoff_zero_intensity', lidar_bp.get_attribute('dropoff_zero_intensity').recommended_values[0])

            for key in sensor_options:
                lidar_bp.set_attribute(key, sensor_options[key])

            lidar = self.world.spawn_actor(lidar_bp, transform, attach_to=attached)

            lidar.listen(self.save_lidar_image)

            return lidar
        
        elif sensor_type == 'SemanticLiDAR':
            lidar_bp = self.world.get_blueprint_library().find('sensor.lidar.ray_cast_semantic')
            lidar_bp.set_attribute('range', '100')

            for key in sensor_options:
                lidar_bp.set_attribute(key, sensor_options[key])

            lidar = self.world.spawn_actor(lidar_bp, transform, attach_to=attached)

            lidar.listen(self.save_semanticlidar_image)

            return lidar
        
        elif sensor_type == "Radar":
            radar_bp = self.world.get_blueprint_library().find('sensor.other.radar')
            for key in sensor_options:
                radar_bp.set_attribute(key, sensor_options[key])

            radar = self.world.spawn_actor(radar_bp, transform, attach_to=attached)
            radar.listen(self.save_radar_image)

            return radar
        
        else:
            return None

    def get_sensor(self):
        return self.sensor

    def save_rgb_image(self, image):
        t_start = self.timer.time()

        image.convert(carla.ColorConverter.Raw)
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]

        if self.display_man.render_enabled() and self.render_enabled:
            self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

        #image.save_to_disk(str(self.save_dir) + f'/rgb/{image.frame}.jpg')
        self.frames_saved += 1

    
    def draw_fov(self):
        max_dist = 30
        og = self.rgb_camera.get_location()
        self.world.debug.draw_point(og, size=0.1, life_time=0.1)
        self.world.debug.draw_point(p1, size=0.1, life_time=0.1, color = carla.Color(255, 0, 0))
        self.world.debug.draw_point(p2, size=0.1, life_time=0.1, color = carla.Color(255, 0, 0))

        self.world.debug.draw_arrow(og, p1, thickness=0.1, color=carla.Color(0,0,255),
                                    life_time=0.1)
        self.world.debug.draw_arrow(og, p2, thickness=0.1, color=carla.Color(0,0,255),
                                    life_time=0.1)

        cam_location = self.sem_camera.get_location()
        cam_location.z = 2
        p1 = carla.Location(cam_location.x + max_dist, cam_location.y - max_dist, 2)
        p2 = carla.Location(cam_location.x + max_dist, cam_location.y + max_dist, 2)

    def save_sem_camera(self, image):
        t_start = self.timer.time()

        image.convert(carla.ColorConverter.CityScapesPalette)
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        
        mask = cv2.imread('./tools/binary_bev_mask.jpg',0)
        res = cv2.bitwise_and(array,array,mask = mask)

        if self.display_man.render_enabled() and self.render_enabled:
            self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))

      #  self.draw_fov()
        #image.save_to_disk(str(self.save_dir) + f'/sem/{image.frame}.jpg')
        self.frames_saved += 1

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

    def save_lidar_image(self, image):
        t_start = self.timer.time()

        disp_size = self.display_man.get_display_size()
        lidar_range = 2.0*float(self.sensor_options['range'])

        points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0] / 4), 4))
        lidar_data = np.array(points[:, :2])
        lidar_data *= min(disp_size) / lidar_range
        lidar_data += (0.5 * disp_size[0], 0.5 * disp_size[1])
        lidar_data = np.fabs(lidar_data)  # pylint: disable=E1111
        lidar_data = lidar_data.astype(np.int32)
        lidar_data = np.reshape(lidar_data, (-1, 2))

        lidar_img_size = (disp_size[0], disp_size[1], 3)
        lidar_img = np.zeros((lidar_img_size), dtype=np.uint8)

        lidar_img[tuple(lidar_data.T)] = (255, 255, 255)

        if self.display_man.render_enabled() and self.render_enabled:
            self.surface = pygame.surfarray.make_surface(lidar_img)

        im = Image.fromarray(lidar_img)
        if image.frame % SAVE_EVERY == 0:
            im.save(str(self.save_dir) + f'/lidar/lidar_{self.frames_saved}.jpg')
            self.frames_saved += 1

        #lidar_img.save_to_disk(str(self.save_dir) + 'lidar/lidar_%6d.jpg' % image.frame)

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

    def save_semanticlidar_image(self, image):
        t_start = self.timer.time()

        disp_size = self.display_man.get_display_size()
        lidar_range = 2.0*float(self.sensor_options['range'])

        points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (int(points.shape[0] / 6), 6))
        lidar_data = np.array(points[:, :2])
        lidar_data *= min(disp_size) / lidar_range
        lidar_data += (0.5 * disp_size[0], 0.5 * disp_size[1])
        lidar_data = np.fabs(lidar_data)  # pylint: disable=E1111
        lidar_data = lidar_data.astype(np.int32)
        lidar_data = np.reshape(lidar_data, (-1, 2))
        lidar_img_size = (disp_size[0], disp_size[1], 3)
        lidar_img = np.zeros((lidar_img_size), dtype=np.uint8)

        lidar_img[tuple(lidar_data.T)] = (255, 255, 255)

        if self.display_man.render_enabled() and self.render_enabled:
            self.surface = pygame.surfarray.make_surface(lidar_img)

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

    def save_radar_image(self, radar_data):
        t_start = self.timer.time()
        points = np.frombuffer(radar_data.raw_data, dtype=np.dtype('f4'))
        points = np.reshape(points, (len(radar_data), 4))

        t_end = self.timer.time()
        self.time_processing += (t_end-t_start)
        self.tics_processing += 1

    def render(self):
        if self.surface is not None:
            offset = self.display_man.get_display_offset(self.display_pos)
            self.display_man.display.blit(self.surface, offset)

    def destroy(self):
        self.sensor.destroy()
