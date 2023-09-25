from simulation import Simulation
from sim_params.front2bev import sim_args

from utils import make_test_dir
from simulation.carla_client import map_layers

sim_args.map = 'TOWN02'

sim_args.test_id = "naked"
sim_args.remove_layers = map_layers.keys()

sim_args.output_path = f"/media/aisyslab/ADATA HD710M PRO/DATASETS/Front2BEV/"
sim_args.frames = 2500


try:
    make_test_dir(sim_args)
    Simulation(sim_args).run()
except KeyboardInterrupt:
    print('\nSimulation interrupted by user.')
