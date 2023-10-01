from sim_params.sensors import sensors
from dan.utils import dict2obj

map = 'Town01'
map_config = 'layers_all'

test_id = 'debug'
output_path = f"_dataset"

ego = {
    'bp': 'charger_2020',
    'sensors': sensors,
    'autopilot': False,
    'speed': 1.0,
}

args = {
    "seed": 42,
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

traffic = {
    'tm_port': 8000,
    'n_vehicles': 30,
    'n_walkers': 10,
    'safe_spawn': True,
    'filterv': 'vehicle.*',
    'generationv': "All",
    'filterw': 'walker.pedestrian.*',
    'generationw': "All",
    'tm_hybrid': False,
    'seedw': 0,

}