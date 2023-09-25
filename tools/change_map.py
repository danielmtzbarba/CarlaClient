#!/usr/bin/env python

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

import carla

def change_map(client, args):
    world = client.load_world(args.map)
    #world.unload_map_layer(carla.MapLayer.Foliage)
    #world.unload_map_layer(carla.MapLayer.Props)


import argparse

def main():
    argparser = argparse.ArgumentParser(
        description='CARLA Change map')
    
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    
    argparser.add_argument(
        '--map',
        metavar='M',
        default='Town01',
        help='Load map (default: Town01)')
    
    args = argparser.parse_args()

    print(args)

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(5.0)
        change_map(client, args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    main()
