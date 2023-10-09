from simulation import start_simulation
from sim_params.front2bev import sim_args

sim_args.reload_map = False
sim_args.map = 'Town01'
sim_args.map_config = "layers_none"
sim_args.test_id = "debug"

sim_args.output_path = "_dataset/Dan-2023-Front2BEV/"
sim_args.frames = 3000

save = False
for s in sim_args.ego.sensors:
    s.save = save

if __name__ == '__main__':
    start_simulation(sim_args)