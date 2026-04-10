# receipt.py
# Grocery Store Receipt Generator
# Author: [Your Name]
# Date: [Current Date]

import csv
from datetime import datetime

def read_dictionary(filename, key_column_index):
    """
    Read a CSV file and create a dictionary where the key is from a specified column.
    
    Parameters:
    filename: The CSV file to read
    key_column_index: The column index to use as dictionary key
    
    Returns:
    A dictionary with keys from the specified column and values as lists of the row data
    """
    product_dict = {}
    
    try:
        with open(filename, 'rt') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row
            
            for row in reader:
                if len(row) > key_column_index:
                    key = row[key_column_index]
                    product_dict[key] = row
                    
    except FileNotFoundError:
        print("Error: missing file")
        print(f"[Errno 2] No such file or directory: '{filename}'")
        raise
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{filename}'.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
        
    return product_dict

def main():
    """
    Main function to process grocery orders and generate receipts.
    """
    try:
        # Store information
        STORE_NAME = "Inkom Emporium"
        SALES_TAX_RATE = 0.06
        
        # Read the product catalog
        PRODUCT_NUM_INDEX = 0
        products_dict = read_dictionary("products.csv", PRODUCT_NUM_INDEX)
        
        # Initialize counters
        total_items = 0
        subtotal = 0.0
        
        # Process the customer order
        with open("request.csv", 'rt') as request_file:
            request_reader = csv.reader(request_file)
            next(request_reader)  # Skip the header row
            
            # Print store name
            print(STORE_NAME)
            
            for row in request_reader:
                if len(row) >= 2:
                    product_number = row[0]
                    quantity = int(row[1])
                    
                    # Look up product in catalog
                    product_info = products_dict[product_number]
                    product_name = product_info[1]
                    price_per_unit = float(product_info[2])
                    
                    # Print item details
                    print(f"{product_name}: {quantity} @ {price_per_unit:.2f}")
                    
                    # Update totals
                    total_items += quantity
                    subtotal += quantity * price_per_unit
                        
    except FileNotFoundError as fnf_error:
        print(f"Error: missing file")
        print(f"[Errno 2] No such file or directory: '{fnf_error.filename}'")
        return
    except PermissionError:
        print("Error: permission denied when trying to read the file.")
        return
    except KeyError as key_error:
        print(f"Error: unknown product ID in the request.csv file")
        print(f"'{key_error}'")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    
    # Calculate tax and total
    sales_tax = subtotal * SALES_TAX_RATE
    total_due = subtotal + sales_tax
    
    # Print summary
    print(f"Number of Items: {total_items}")
    print(f"Subtotal: {subtotal:.2f}")
    print(f"Sales Tax: {sales_tax:.2f}")
    print(f"Total: {total_due:.2f}")
    print(f"Thank you for shopping at the {STORE_NAME}.")
    
    # Print current date and time
    current_datetime = datetime.now()
    print(current_datetime.strftime("%a %b %d %H:%M:%S %Y"))

if __name__ == "__main__":
    main()