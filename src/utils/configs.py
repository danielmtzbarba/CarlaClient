import os, ast
import pandas as pd
from yacs.config import CfgNode
from argparse import ArgumentParser

def load_config(config_path):
    with open(config_path) as f:
        return CfgNode.load_cfg(f)

def get_default_configuration():
    root = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
    defaults_path = os.path.join(root, 'configs/config.yml')
    return load_config(defaults_path)

def get_console_args():
    parser = ArgumentParser()

    parser.add_argument('--map', default='Town01', 
                        help='Map')
    parser.add_argument('--reload', default=0, 
                        help='reload world?')
    parser.add_argument('--map_config', default='layers_all', 
                        help='Map layers')
    parser.add_argument('--scene', default=1, 
                        help='Route or Scene')

    parser.add_argument('--experiment', default='test', 
                        help='name of experiment config to load')
    parser.add_argument('--sensors', choices=['front2bev', 'all'],
                        default='front2bev', help='sensor suite setup')
    parser.add_argument('--pc', default='aisyslab', 
                        help='machine config')
    return parser.parse_args()

def get_configuration():

    args = get_console_args()

    # Load config defaults
    config = get_default_configuration()
    
    # PC
    config.merge_from_file(f'configs/pc/{args.pc}.yml')
    #
    config.merge_from_file(f'configs/sensors/{args.sensors}.yml')
    # Load experiment options
    config.merge_from_file(f'configs/experiments/{args.experiment}.yml')

    # Override with command line options
    config.map = args.map
    if args.reload == "True":
        config.reload_map = True 
    else:
        config.reload_map = False 
    config.map_config = args.map_config
    config.n_scene = args.scene

    config.merge_from_file(f'configs/scenes/{config.map}/seq{config.n_scene}.yml')

    if config.save:
        config.logdir = create_experiment(config)

    # Finalise config
    config.freeze()

    return config

def create_experiment(config):
    logdir = os.path.join(os.path.expandvars(config.logdir),
                          config.map, f'scene_{config.n_scene}', config.map_config)
    print("\n==> Creating new experiment in directory:\n" + logdir)
    try:
        os.makedirs(logdir)
    except:
        # Directory exists
        pass
         # Save the current config
        with open(os.path.join(logdir, 'config.yml'), 'w') as f:
             f.write(config.dump())

    print(config.name, config.map_config)
    
    return logdir
