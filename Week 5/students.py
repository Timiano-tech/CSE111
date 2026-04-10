import csv

def main():
    # ===========================================
    # PART 1: Read CSV file into dictionary
    # ===========================================
    students = {}
    
    with open('students.csv', 'r') as file:
        reader = csv.reader(file)
        
        # Skip the header row (I-Number,Name)
        next(reader)
        
        # Store each ID as key and name as value
        for row in reader:
            id_number = row[0]
            name = row[1]
            students[id_number] = name
    
    # ===========================================
    # PART 2: Get and validate user input
    # ===========================================
    print("\n--- Student Lookup System ---")
    print("Enter 'quit' at any time to exit.\n")
    
    while True:
        # Get ID from user
        id_input = input("Enter student ID Number: ").strip()
        
        # Creative enhancement: Allow user to quit
        if id_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        # Enhancement 1: Remove dashes
        id_cleaned = id_input.replace('-', '')
        
        # Enhancement 2: Validation
        valid = True
        
        # Check for non-digit characters
        if not id_cleaned.isdigit():
            print("Invalid ID Number")
            valid = False
        
        # Check length (assuming standard 9-digit format)
        elif len(id_cleaned) < 9:
            print("Invalid ID Number: too few digits")
            valid = False
        
        elif len(id_cleaned) > 9:
            print("Invalid ID Number: too many digits")
            valid = False
        
        # If valid, look up in dictionary
        if valid:
            if id_cleaned in students:
                # Creative enhancement: Format output nicely
                print(f"Student found: {students[id_cleaned]}")
            else:
                print("No such student")
        
        print()  # Blank line for readability

if __name__ == "__main__":
    main()