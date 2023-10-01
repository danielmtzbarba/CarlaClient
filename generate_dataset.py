from simulation import start_simulation
from sim_params.front2bev import sim_args
from simulation.map import maps

sim_args.output_path = f"/media/aisyslab/ADATA HD710M PRO/DATASETS/Front2BEV/"

map_configs = [['layers_none', 2000],
               ['layers_all', 2000]]

if __name__ == '__main__':

    for map in maps:
        sim_args.map = map
        for config in map_configs:
            sim_args.test_id = config[0]
            sim_args.map_config = config[0]
            sim_args.frames = config[1]

            start_simulation(sim_args)