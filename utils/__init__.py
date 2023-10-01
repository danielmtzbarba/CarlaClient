from dan.utils import make_folder

dir_list = ['rgb', 'rgbd', 'sem', 'lidar', 'bev']

def make_test_dir(sim_args):
    map_path = make_folder(sim_args.output_path, sim_args.map)
    test_path = make_folder(map_path, sim_args.test_id)

    for dir in dir_list:
        make_folder(test_path, dir)
