import sys, os, glob

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla, pygame

from simulation.sync_mode import CarlaSyncMode
from simulation.display import Display

class Simulation(object):
    def __init__(self, sim_args):
        self.args = sim_args
    
    def exit_sim(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return True
        return False
    
    def run(self):
        pygame.init()
        self.display = Display(self.args.window_size)
        try:

            # Create a synchronous mode context.
            with CarlaSyncMode(self.args, fps=30) as sync_mode:
                # Simulation loop
                while True:

                    if self.exit_sim():
                        return
                    self.display.clock.tick()

                    sync_mode.ego_next_waypoint()

                    # Advance the simulation and wait for the data.
                    snapshot, image_rgb, image_semseg = sync_mode.tick(timeout=2.0)

                    # Draw the pygame display.
                    self.display.draw_display(snapshot, image_rgb, image_semseg)
                    # Update the pygame display
                    self.display.update()
                        
        finally:
            pygame.quit()
            print('Simulation ended.')