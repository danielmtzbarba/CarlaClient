from simulation import start_simulation
from sim_params.front2bev import sim_args

sim_args.map = 'Town10HD'

sim_args.test_id = "layers_all"
sim_args.map_config = "layers_all"

sim_args.output_path = "/media/aisyslab/ADATA HD710M PRO/DATASETS/Front2BEV/"
sim_args.frames = 2000

if __name__ == '__main__':
    start_simulation(sim_args)