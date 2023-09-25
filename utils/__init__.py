from dan.utils import make_folder

def make_test_dir(sim_args):
    map_path = make_folder(sim_args.output_path, sim_args.map)
    test_path = make_folder(map_path, sim_args.test_id)

    for sensor_args in sim_args.ego.sensors:
        make_folder(test_path, sensor_args.id)
