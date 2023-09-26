from simulation.map import load_map
from utils import make_test_dir
from simulation.simulation import Simulation

def start_simulation(sim_args):
    """
    Args:
        sim_args (_type_): _description_
    """

    # First load empty map, and load
    # the necessary layers.
    load_map(sim_args)

    # Create the test output directory.
    make_test_dir(sim_args)

    # Then, run the simulation.
    try:
        Simulation(sim_args).run()
    except KeyboardInterrupt:
        print('\nSimulation interrupted by user.')
    
    print('\nSimulation completed successfully.')