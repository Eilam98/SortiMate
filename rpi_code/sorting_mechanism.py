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
    PLASTIC = 1
    PAPER = 2
    ALUMINUM = 3
    OTHER = 4

class SortingMechanism:
    """
    A class to control the sorting mechanism using two servo motors.
    
    Attributes:
        rotation_servo (ServoController): Servo motor for rotating the sorting pipe
        gate_servo (ServoController): Servo motor for controlling the waste gate
        bin_angles (Dict[WasteType, float]): Mapping of waste types to rotation angles
    """
    
    def __init__(self, rotation_pin: int, gate_pin: int):
        """
        Initialize the sorting mechanism.
        
        Args:
            rotation_pin (int): GPIO pin for the rotation servo
            gate_pin (int): GPIO pin for the gate servo
        """
        self.rotation_servo = ServoController(rotation_pin)
        self.gate_servo = ServoController(gate_pin)
        
        # Define angles for each bin position
        self.bin_angles = {
            WasteType.PLASTIC: 0,
            WasteType.PAPER: 90,
            WasteType.ALUMINUM: 180,
            WasteType.OTHER: 270
        }
        
        # Initialize servos to home position
        self.rotation_servo.set_angle(0)
        self.gate_servo.set_angle(0)
    
    def sort_waste(self, waste_type: WasteType) -> None:
        """
        Sort waste into the appropriate bin.
        
        Args:
            waste_type (WasteType): Type of waste to sort
            
        Raises:
            ValueError: If waste_type is not a valid WasteType
        """
        if waste_type not in self.bin_angles:
            raise ValueError(f"Invalid waste type: {waste_type}")
        
        # Move rotation servo to correct bin position
        target_angle = self.bin_angles[waste_type]
        self.rotation_servo.set_angle(target_angle)
        
        # Open gate to drop waste
        self.gate_servo.set_angle(90)  # Open gate
        time.sleep(1)  # Wait for waste to drop
        self.gate_servo.set_angle(0)   # Close gate
    
    def cleanup(self) -> None:
        """Clean up GPIO resources for both servos."""
        self.rotation_servo.cleanup()
        self.gate_servo.cleanup() 