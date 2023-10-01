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

sensors = [rgb_ex, semseg_ex]