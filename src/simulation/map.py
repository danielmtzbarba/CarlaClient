import carla
from src.simulation.utils import map_layers

maps = ['Town01','Town02', 'Town03', 'Town04', 'Town05', 'Town06','Town07','Town10HD']

map_configs = {
    'layers_none': [carla.MapLayer.Ground],

    'layers_all': [
        carla.MapLayer.Particles,
        carla.MapLayer.Buildings,
        carla.MapLayer.Ground,
        carla.MapLayer.Walls,
        carla.MapLayer.Decals,
        carla.MapLayer.Foliage,
        carla.MapLayer.ParkedVehicles,
        carla.MapLayer.Props,
    ],

    'traffic': [
        carla.MapLayer.Particles,
        carla.MapLayer.Buildings,
        carla.MapLayer.Ground,
        carla.MapLayer.Walls,
        carla.MapLayer.Decals,
        carla.MapLayer.Foliage,
        carla.MapLayer.ParkedVehicles,
        carla.MapLayer.Props,
    ],
}

def load_map_layers(world, map_config): 
    map_config = map_configs[map_config]
    if "Opt" in str(world.get_map()):
        for layer in map_config:
            world.load_map_layer(layer)
    return True

def load_map(args):
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)

        world = client.load_world(f"{args.map}_Opt",
                                  map_layers=carla.MapLayer.NONE)
        map = world.get_map()
        print("Loaded map: ", str(map))
        load_map_layers(world, args.map_config)
    except:
        print('\n. Error: Could not load map!')
