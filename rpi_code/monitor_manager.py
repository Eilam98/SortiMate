# monitor_manager.py

import os
import pygame

class MonitorManager:
    """Displays one image/GIF per program state, on HDMI-1 (:0.1)."""

    def __init__(
        self,
        images_dir: dict,
        window_size: tuple = (800, 600),
        display: str = ":0.0",
        monitor_index: int = 1,
    ):
        """
        :param images_dir: mapping state_name -> single image/GIF file path
        :param window_size: (w, h) in pixels
        :param display: X11 display (always :0.0)
        :param monitor_index: SDL video display index (0 → HDMI-1, 1 → HDMI-2)
        """
        os.environ["DISPLAY"] = display
        os.environ["SDL_VIDEO_FULLSCREEN_DISPLAY"] = str(monitor_index)
        # Additional environment variables to ensure proper display selection
        os.environ["SDL_VIDEO_WINDOW_POS"] = "800,0"  # Position window on HDMI-2 (offset by HDMI-1 width)
        pygame.init()
        flags = pygame.FULLSCREEN | pygame.NOFRAME
        self.screen = pygame.display.set_mode(window_size, flags=flags)
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