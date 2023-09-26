# carla-scripts
Scripts for Carla Simulator

## Camera Parameters
```
camera.set_attribute('image_size_x', '1024')
camera.set_attribute('image_size_y', '1024')
camera.set_attribute('fov', str(90.0))
```

### RGB Front View Camera 
```
carla.Transform(carla.Location(x=0.0, y=0.0, z=2.0), carla.Rotation(pitch=-90, yaw=+00, roll=+00))
```

### Bird View Ground Truth Camera
```
carla.Transform(carla.Location(x=0.0, y=0.0, z=32.0), carla.Rotation(yaw=+00, pitch=-90))
```
