from simulation import start_simulation
from sim_params.front2bev import sim_args

sim_args.display = False

sim_args.reload_map = True
sim_args.map = 'Town02'
sim_args.ego.route = 'sim_params/routes/front2bev_town02.npy'
sim_args.map_config = "layers_all"
sim_args.test_id = "layers_all"

sim_args.output_path = "/media/dan/dan/Datasets/Dan-2023-Front2BEV/"
sim_args.frames = 10000

save = True
for s in sim_args.ego.sensors:
    s.save = save

if __name__ == '__main__':
    start_simulation(sim_args)