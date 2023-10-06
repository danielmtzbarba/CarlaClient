from dan.utils import make_folder

def make_test_dir(sim_args):
    map_path = make_folder(sim_args.output_path, sim_args.map)
    test_path = make_folder(map_path, sim_args.test_id)

    for sensor in sim_args.ego.sensors:
        if sensor.save:
            sensor_path = make_folder(test_path, sensor.id)

            if sensor.id == 'bev':
                make_folder(sensor_path, 'sem')

    
