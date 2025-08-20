# monitor_manager.py

import os
import pygame

class MonitorManager:
    """Displays one image/GIF per program state, on HDMI-1 (:0.1)."""

    def __init__(
        self,
        window_size: tuple = (1920, 1080),
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

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # get the directory where main.py lives
        self.IMG  = os.path.join(self.BASE_DIR, "monitor_images")
        self.images_dirs = {
            "default":      os.path.join(self.IMG, "default.png"),
            "classifying":  os.path.join(self.IMG, "classifying.png"),
            "Plastic":      os.path.join(self.IMG, "plastic.png"),
            "Glass":        os.path.join(self.IMG, "glass.png"),
            "Metal":        os.path.join(self.IMG, "metal.png"),
            "Other":        os.path.join(self.IMG, "other.png"),
            "summary":      os.path.join(self.IMG, "summary.png"),
            "active_session": os.path.join(self.IMG, "active_session.png"),
            "low_confidence": os.path.join(self.IMG, "low_confidence.png"),
        }

        # load + scale each image/GIF once
        self.images = {}
        for state, image_dir in self.images_dirs.items():
            img = pygame.image.load(image_dir)
            self.images[state] = pygame.transform.scale(img, window_size)
        
        self.current_state = "default"

    def show(self, state: str):
        """Immediately switch to and display the given state."""
        frame = self.images.get(state)
        if not frame:
            raise ValueError(f"Unknown state: {state!r}")
        self.screen.blit(frame, (0, 0))
        pygame.display.flip()
        self.current_state = state

    def stop(self):
        """Cleanup at program exit."""
        pygame.quit()
    
    def check_and_update_active_user_state(self, active_user):
        """
        Check if monitor should be updated based on active_user state.
        Only updates if currently showing default/active_session states.
        """
        if self.current_state in ["default", "active_session"]:
            new_state = "active_session" if active_user else "default"
            if new_state != self.current_state:
                self.show(new_state)
                return True
        return False

    def current_monitor_default(self, state, current_active_user_state):
        """Update monitor display considering active_user state"""
        if state == "default" and current_active_user_state:
            self.show("active_session")
        else:
            self.show(state)