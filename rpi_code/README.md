# Smart Automatic Recycling Sorting Bin - RPi Control Code

This is the Raspberry Pi control code for the Smart Automatic Recycling Sorting Bin project. The code manages the servo motors that control the sorting mechanism for different types of recyclable materials.

## Hardware Requirements

- Raspberry Pi 3B+
- 2x Deegoo-FPV MG996R Servo Motors
- Jumper wires
- Power supply for servos (5V)

## Pin Configuration

- Rotation Servo: GPIO17 (Pin 11)
- Gate Servo: GPIO27 (Pin 13)

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Connect the servo motors to the specified GPIO pins:
   - Rotation Servo: Connect to GPIO17 (Pin 11)
   - Gate Servo: Connect to GPIO27 (Pin 13)
   - Power: Connect to 5V
   - Ground: Connect to GND

3. Run the program:
   ```bash
   python main.py
   ```

## Code Structure

- `servo_controller.py`: Base class for controlling individual servo motors
- `sorting_mechanism.py`: Class that coordinates the two servo motors for waste sorting
- `main.py`: Main script demonstrating the sorting mechanism
- `requirements.txt`: List of Python dependencies

## Usage

The program demonstrates the sorting mechanism by cycling through all waste types:
1. Plastic
2. Paper
3. Aluminum
4. Other

To stop the program, press Ctrl+C.

## Notes

- The servo angles are configured for a specific physical setup. You may need to adjust the angles in `sorting_mechanism.py` based on your actual bin positions.
- Make sure the Raspberry Pi has sufficient power to drive the servos.
- The program includes proper cleanup of GPIO resources when interrupted. 