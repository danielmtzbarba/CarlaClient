rgb_ex = {
    "id": 'rgb',
    "bp": 'sensor.camera.rgb',

    "location": (-5.5, 0.0, 2.8),
    'rotation': (0.0, -15, 0.0),

    'params':{
        'image_size_x': "512",
        'image_size_y': "512",
    },

    'save': True,
}

semseg_ex = {
    "id": 'sem',
    "bp": 'sensor.camera.semantic_segmentation',
    "location": (-5.5, 0.0, 2.8),
    'rotation': (0.0, -15, 0.0),

    'params':{
        'image_size_x': "512",
        'image_size_y': "512",
    },

    'save': True,
}

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

bev_sem_camera = {
    "id": 'sem',
    "bp": 'sensor.camera.semantic_segmentation',
    "location": (0.0, 0.0, 32.0),
    'rotation': (-90.0, 0.0, 0.0),

    'params':{
        'image_size_x': "1024",
        'image_size_y': "1024",
    },

    'save': True,
}