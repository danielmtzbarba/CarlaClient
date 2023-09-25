from dan.utils import dict2obj

from sim_params.sensors import sensors

map = 'debug'
test_id = "debug"
output_path = f"_dataset"

ego = {
    'bp': 'charger_2020',
    'sensors': sensors,
    'autopilot': False,
}

args = {
    "test_id": test_id,
    "output_path": output_path,

    'map': map,
    'remove_layers': [],
    'ego': ego,

    'grid_size': [1,1],
    'window_size': (1024, 1024),

    'frames': -1,
}    

sim_args = dict2obj(args)