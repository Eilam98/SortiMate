import time
from sorting_mechanism import SortingMechanism, WasteType

def main():
    try:
        sorter = SortingMechanism(rotation_pin=17, gate_pin=27) # GPIO17 for rotation servo, GPIO27 for gate servo
        waste_types = [
            (WasteType.PLASTIC, "Plastic"),
            (WasteType.PAPER, "Paper"),
            (WasteType.ALUMINUM, "Aluminum"),
            (WasteType.OTHER, "Other")
        ]
        print("Smart Recycling Bin initialized...")
        
        for waste_type, name in waste_types:
            print(f"\nSorting {name}...")
            sorter.sort_waste(waste_type)
            time.sleep(2)  # Wait between demonstrations
        
        print("\nDemonstration complete!")
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up GPIO resources
        sorter.cleanup()

if __name__ == "__main__":
    main() 