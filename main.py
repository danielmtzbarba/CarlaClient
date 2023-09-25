from simulation import Simulation
from sim_params.default import sim_args

from utils import make_test_dir

try:
    make_test_dir(sim_args)
    Simulation(sim_args).run()

except KeyboardInterrupt:
    print('\nSimulation interrupted by user.')
