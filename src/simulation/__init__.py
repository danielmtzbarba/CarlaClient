from src.simulation.map import load_map
from src.simulation.simulation import Simulation

def start_simulation(config):
    """
    Args:
        config (_type_): _description_
    """
    
    #  Reload map?
    if config.reload_map:
        # First load empty map, then, 
        # load configured layers.
        load_map(config)
    
    # Then, run the simulation.
    try:
        Simulation(config).run()
    except KeyboardInterrupt:
        print('\nSimulation interrupted by user.')
    
    print('\nSimulation completed successfully.')
