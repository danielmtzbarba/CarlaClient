from simulation import start_simulation
from sim_params.front2bev import sim_args

sim_args.map = 'Town01'

sim_args.test_id = "debug"
sim_args.map_config = "layers_all"

sim_args.output_path = "/media/dan/BICHO/Datasets/Dan-2023-Front2BEV"
sim_args.frames = 2000

if __name__ == '__main__':
    start_simulation(sim_args)