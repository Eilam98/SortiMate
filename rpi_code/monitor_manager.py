# monitor_manager.py

import os
import pygame

class MonitorManager:
    """Displays one image/GIF per program state, on HDMI-1 (:0.1)."""

    def __init__(
        self,
        images_dir: dict,
        window_size: tuple = (800, 600),
        display: str = ":0.1",
    ):
        """
        :param images_dir: mapping state_name -> single image/GIF file path
        :param window_size: (w, h) in pixels
        :param display: X11 display for the second monitor
        """
        os.environ["DISPLAY"] = display
        pygame.init()
        self.screen = pygame.display.set_mode(window_size, flags=pygame.NOFRAME)
        pygame.display.set_caption("Recycling Bin Monitor")

        # load + scale each image/GIF once
        self.images = {}
        for state, image_dir in images_dir.items():
            img = pygame.image.load(image_dir)
            self.images[state] = pygame.transform.scale(img, window_size)

    def show(self, state: str):
        """Immediately switch to and display the given state."""
        frame = self.images.get(state)
        if not frame:
            raise ValueError(f"Unknown state: {state!r}")
        self.screen.blit(frame, (0, 0))
        pygame.display.flip()

    def stop(self):
        """Cleanup at program exit."""
        pygame.quit()