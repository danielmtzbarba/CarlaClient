import pygame 
import numpy as np

pygame_font = pygame.font.match_font('ubuntumono')

class Display(object):
    def __init__(self, window_size=(800, 600)):
        self.display = pygame.display.set_mode(window_size,
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame_font, 14)

    def draw_image(self, image, blend=False):
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        if blend:
            image_surface.set_alpha(100)
        self.display.blit(image_surface, (0, 0))

    def draw_display(self,  snapshot, image_rgb, image_semseg):
        fps = round(1.0 / snapshot.timestamp.delta_seconds)

        # Draw the display.
        self.draw_image(image_semseg)
    #    self.draw_image(image_semseg, blend=True)
        self.display.blit(
            self.font.render('% 5d FPS (real)' % self.clock.get_fps(), True, (255, 255, 255)),
            (8, 10))
        self.display.blit(
            self.font.render('% 5d FPS (simulated)' % fps, True, (255, 255, 255)),
            (8, 28))
    
    def update(self):
        pygame.display.flip()



   
