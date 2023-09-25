front_rgb_camera = {
    "id": 'rgb',
    "bp": 'sensor.camera.rgb',
    "location": (0.0, 0.0, 2.0),
    'rotation': (0.0, 0.0, 0.0),

    'params':{
        'image_size_x': "1024",
        'image_size_y': "1024",
        'fov': "90.0",
    },

    'save': True,
}

front_sem_camera = {
    "id": 'sem',
    "bp": 'sensor.camera.semantic_segmentation',
    "location": (0.0, 0.0, 2.0),
    'rotation': (0.0, 0.0, 0.0),

    'params':{
        'image_size_x': "1024",
        'image_size_y': "1024",
        'fov': "90.0",
    },

    'save': True,
}

front_rgbd_camera = {
    "id": 'rgbd',
    "bp": 'sensor.camera.depth',
    "location": (0.0, 0.0, 2.0),
    'rotation': (0.0, 0.0, 0.0),

    'params':{
        'image_size_x': "1024",
        'image_size_y': "1024",
        'fov': "90.0",
    },

    'save': True,
}

bev_sem_camera = {
    "id": 'bev',
    "bp": 'sensor.camera.semantic_segmentation',
    "location": (0.0, 0.0, 32.0),
    'rotation': (-90.0, 0.0, 0.0),

    'params':{
        'image_size_x': "1024",
        'image_size_y': "1024",
    },

    'save': True,
}

lidar_3d = {
    "id": 'lidar',
    "bp": 'sensor.lidar.ray_cast',
    "location": (0.0, 0.0, 2.0),
    'rotation': (0.0, 0.0, 0.0),

    'params':{
        'upper_fov': '15.0',
        'lower_fov': '-30.0',
        'channels': '64',
        'range': '100.0',
        'rotation_frequency': '30',
        'points_per_second': '500000',

        # NO NOISE
        'dropoff_general_rate': '0.0',
        'dropoff_intensity_limit': '1.0',
        'dropoff_zero_intensity': '0.0',

        # WITH NOISE
        #'noise_stddev': '0.2',
    },

    'lidar_img_x': 1024,
    'lidar_img_y': 1024,

    'save': True,
}

sensors = [front_rgb_camera, front_sem_camera,
           front_rgbd_camera, bev_sem_camera, lidar_3d]