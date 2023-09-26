from sim_params.sensors.front2bev import sensors
from dan.utils import dict2obj

map = 'Town01'
map_config = 'all'

test_id = 'debug'
output_path = f"_dataset"

ego = {
    'bp': 'charger_2020',
    'sensors': sensors,
    'autopilot': False,
    'speed': 1.0,
}

args = {
    "test_id": test_id,
    "output_path": output_path,

    'map': map,
    'map_config': map_config,
    'ego': ego,

    'grid_size': [1,1],
    'window_size': (1024, 1024),

    'frames': -1,

}    

sim_args = dict2obj(args)
