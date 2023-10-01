import carla

map_layers = {
    'All': carla.MapLayer.All,
    'None': carla.MapLayer.NONE,
    'Particles': carla.MapLayer.Particles,
    'Buildings': carla.MapLayer.Buildings,
    'Ground': carla.MapLayer.Ground,
    'Walls': carla.MapLayer.Walls,
    'Decals': carla.MapLayer.Decals,
    'Foliage': carla.MapLayer.Foliage,
    'ParkedVehicles': carla.MapLayer.ParkedVehicles,
    'Props': carla.MapLayer.Props,
    'StreetLights': carla.MapLayer.StreetLights,
}

envobj_tags = {
    'Vegetation':  carla.CityObjectLabel.Vegetation,
    'Buildings': carla.CityObjectLabel.Buildings,
    'Bridge': carla.CityObjectLabel.Bridge,
    'Walls': carla.CityObjectLabel.Walls,
    'Fences': carla.CityObjectLabel.Fences,

    'TraffiSigns': carla.CityObjectLabel.TrafficSigns,
    'Poles': carla.CityObjectLabel.Poles,
    'RoadLines': carla.CityObjectLabel.RoadLines,
    'GuardRail': carla.CityObjectLabel.GuardRail,
    'RailTrack': carla.CityObjectLabel.RailTrack,
    'Static': carla.CityObjectLabel.Static,
    'Dynamic': carla.CityObjectLabel.Dynamic, 
    'Other': carla.CityObjectLabel.Other,
}