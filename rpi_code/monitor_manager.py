import os
import threading
import time
import pygame

class MonitorManager:
    """
    Manages a fullscreen slideshow on a second HDMI-connected monitor.
    States: 'default', 'classifying', 'Plastic', 'Glass', 'Metal', 'Other', 'summary'.
    """

    def __init__(
        self,
        image_dirs: dict,
        interval: float = 5.0,
        window_size: tuple = (800, 600),
        display: str = ":0.1",
    ):
        """
        :param image_dirs: mapping state_name -> list of image/GIF file paths
        :param interval: seconds between frames
        :param window_size: (width, height) in pixels
        :param display: X DISPLAY for second monitor, e.g. ":0.1"
        """
        # target second screen
        os.environ["DISPLAY"] = display

        # initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(window_size, flags=pygame.NOFRAME)
        pygame.display.set_caption("Recycling Bin Monitor")

        self.interval = interval
        self.window_size = window_size
        self.image_dirs = image_dirs

        # load and scale all images into memory
        self.images = {}
        for state, paths in image_dirs.items():
            frames = []
            for path in paths:
                img = pygame.image.load(path)
                frames.append(pygame.transform.scale(img, window_size))
            self.images[state] = frames

        # threading primitives
        self._lock = threading.Lock()
        self.current_state = "default"
        self._index = 0
        self._running = False
        self._thread = threading.Thread(target=self._run_loop, daemon=True)

    def start(self):
        """Begin the display thread."""
        self._running = True
        self._thread.start()

    def stop(self):
        """Stop the display thread and close the window."""
        self._running = False
        self._thread.join()
        pygame.quit()

    def set_state(self, state: str):
        """
        Switch to a new state—will restart that state's frame sequence.
        Valid states are the keys of image_dirs passed into __init__.
        """
        with self._lock:
            if state in self.images:
                self.current_state = state
                self._index = 0

    def _run_loop(self):
        """Background loop that blits the current frame, updates index, and sleeps."""
        while self._running:
            with self._lock:
                frames = self.images.get(self.current_state, [])
                if frames:
                    frame = frames[self._index]
                    self.screen.blit(frame, (0, 0))
                    pygame.display.flip()
                    self._index = (self._index + 1) % len(frames)
            time.sleep(self.interval)