from dan.utils import dict2obj

from sim_params.sensors import front_rgb_camera, bev_sem_camera

map = 'TOWN07'
test_id = "debug"
output_path = f"_dataset"

ego = {
    'bp': 'charger_2020',
    'sensors': [front_rgb_camera, bev_sem_camera],
    'autopilot': False,
}

args = {
    "test_id": test_id,
    "output_path": output_path,

    'map': map,
    'remove_layers': ['Vegetation', 'Poles'],
    'ego': ego,

    'grid_size': [1,1],
    'window_size': (1024, 1024)

}    

sim_args = dict2obj(args)