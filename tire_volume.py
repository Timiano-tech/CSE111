# tire_volume.py
# This program calculates the volume of a tire based on user input
# and records the information in a text file.
# 
# Enhancement: After calculating the volume, the program asks if the user
# wants to buy tires with those dimensions. If yes, it asks for their
# phone number and stores it in the volumes.txt file along with the
# tire information. This helps the tire company contact potential customers.

from datetime import datetime
import math

def main():
    # Get user input for tire measurements
    print("Welcome to the Tire Volume Calculator!")
    print("This program will calculate the approximate volume of space inside a tire.")
    print()
    
    # Get width from user
    width = float(input("Enter the width of the tire in mm (ex 205): "))
    
    # Get aspect ratio from user
    aspect_ratio = float(input("Enter the aspect ratio of the tire (ex 60): "))
    
    # Get diameter from user
    diameter = float(input("Enter the diameter of the wheel in inches (ex 15): "))
    
    # Calculate the tire volume using the formula from the assignment
    # v = (π * w^2 * a * (w * a + 2540 * d)) / 10,000,000,000
    # I had to look at the formula a few times to make sure I got it right
    
    # First part: π * w^2 * a
    part1 = math.pi * (width ** 2) * aspect_ratio
    
    # Second part: w * a + 2540 * d
    part2 = (width * aspect_ratio) + (2540 * diameter)
    
    # Multiply part1 and part2, then divide by 10,000,000,000
    volume = (part1 * part2) / 10000000000
    
    # Round to 2 decimal places
    volume_rounded = round(volume, 2)
    
    # Display the result to the user
    print()
    print(f"The approximate volume is {volume_rounded} liters")
    
    # Get current date from computer
    current_date = datetime.now()
    # Format the date as YYYY-MM-DD (no time)
    date_formatted = f"{current_date:%Y-%m-%d}"
    
    # Append the data to volumes.txt file
    with open("volumes.txt", "at") as volumes_file:
        # Write the tire information to the file
        print(f"{date_formatted}, {width}, {aspect_ratio}, {diameter}, {volume_rounded}", file=volumes_file)
    
    # Enhancement: Ask if user wants to buy tires
    print()
    buy_response = input("Would you like to buy tires with these dimensions? (yes/no): ")
    
    # Check if user wants to buy (case insensitive)
    if buy_response.lower() == "yes" or buy_response.lower() == "y":
        # Get phone number from user
        phone_number = input("Please enter your phone number so we can contact you: ")
        
        # Append phone number to the same file (with a note that it's a potential customer)
        with open("volumes.txt", "at") as volumes_file:
            # Write the phone number on a new line with a timestamp
            print(f"Phone number for potential customer ({date_formatted}): {phone_number}", file=volumes_file)
        
        print("Thank you! A representative will contact you soon.")
    else:
        print("No problem. Thank you for using the Tire Volume Calculator!")
    
    print()
    print("Your tire information has been saved to volumes.txt")

# Call the main function to start the program
if __name__ == "__main__":
    main() 