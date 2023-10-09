from simulation import start_simulation
from sim_params.front2bev import sim_args

sim_args.display = False

sim_args.reload_map = False
sim_args.map = 'Town03'
sim_args.route = 'sim_params/routes/front2bev_town03.npy'
sim_args.map_config = "layers_none"
sim_args.test_id = "debug"

sim_args.output_path = "/media/aisyslab/dan/Datasets/Dan-2023-Front2BEV/"
sim_args.frames = 10000

save = False
for s in sim_args.ego.sensors:
    s.save = save

if __name__ == '__main__':
    start_simulation(sim_args)