import sys, os, glob

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import pygame

from src.simulation.sync_mode import CarlaSyncMode
from src.simulation.display import Display

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
        if self.args.display:
            self.display = Display(self.args.window_size)
        try:

            # Create a synchronous mode context.
            with CarlaSyncMode(self.args, fps=30) as sync_mode:
                # Simulation loop
                while True:

                    if self.exit_sim() or sync_mode.exit:
                        return

                    if not self.args.ego.autopilot:
                        next_wp = sync_mode.ego_next_waypoint()
                        sync_mode.ego_move(next_wp)

                    # Advance the simulation and wait for the data.
                    data = sync_mode.tick(timeout=10.0)

                    if self.args.display:
                        # Draw the pygame display.
                        self.display.clock.tick()

                        self.display.draw_display(data[0], data[1])
                        # Update the pygame display
                        self.display.update()

                    if sync_mode.n_frame == self.args.frames:
                        return
                        
        finally:
            pygame.quit()
            print('Simulation ended.')
