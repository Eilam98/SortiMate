"""
Sorting mechanism controller for the recycling bin.
This module manages the coordination between two servo motors for waste sorting.
"""

from enum import Enum
from typing import Dict
from servo_controller import ServoController
import time

class WasteType(Enum):
    """Enumeration of possible waste types."""
    GLASS = 1
    PLASTIC = 2
    METAL = 3
    OTHER = 4

class SortingMechanism:
    """
    A class to control the sorting mechanism using two servo motors.

    """
    
    def __init__(self, rotation_pin: int, gate_pin: int):
        """
        Initialize the sorting mechanism.
        
        """
        self.rotation_servo = ServoController(rotation_pin, home_position=90)
        self.gate_servo = ServoController(gate_pin, home_position=0)
        
        # Define angles for each bin position
        self.bin_angles = { # TO FIX: angles and enum
            WasteType.GLASS: 0,
            WasteType.PLASTIC: 60,
            WasteType.METAL: 120,
            WasteType.OTHER: 180
        }
        
        # Initialize servos to home position
        self.rotation_servo.set_angle(self.rotation_servo.home_position)
        self.gate_servo.set_angle(self.gate_servo.home_position)
    
    def sort_waste(self, waste_type: WasteType) -> None:
        """
        Sort waste into the appropriate bin.
        """
        if waste_type not in self.bin_angles:
            raise ValueError(f"Invalid waste type: {waste_type}")
        
        # Move rotation servo to correct bin position
        target_angle = self.bin_angles[waste_type]
        self.rotation_servo.set_angle(target_angle)
        time.sleep(1)  # Wait for pipe to rotate
        self.gate_servo.set_angle(150)  # Open gate
        time.sleep(1)  # Wait for waste to drop
        self.gate_servo.set_angle(self.gate_servo.home_position)
        self.rotation_servo.set_angle(self.rotation_servo.home_position)
    
    def cleanup(self) -> None:
        """Clean up GPIO resources for both servos."""
        #TO ADD: self.rotation_servo.cleanup()
        self.gate_servo.cleanup() 