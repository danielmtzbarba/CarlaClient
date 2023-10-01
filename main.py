from simulation import start_simulation
from sim_params.front2bev import sim_args

sim_args.reload_map = True
sim_args.map = 'Town03'
sim_args.map_config = "layers_all"
sim_args.test_id = "debug"

sim_args.output_path = "/media/dan/BICHO/Datasets/Dan-2023-Front2BEV"
sim_args.frames = 2000

if __name__ == '__main__':
    start_simulation(sim_args)