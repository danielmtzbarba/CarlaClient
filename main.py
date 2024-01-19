# -----------------------------------------------------------------------------
import random
from src.simulation import start_simulation
from src.utils import configs
# -----------------------------------------------------------------------------

def main(config: object):
    random.seed(config.seed)
    start_simulation(config)

if __name__ == '__main__':
    config = configs.get_configuration()
    main(config)  

