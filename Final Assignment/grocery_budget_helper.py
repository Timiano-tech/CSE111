# grocery_budget_helper.py
# CSE 111 - Grocery Budget Helper
# This program helps compare grocery prices between two stores
# Author: Ajayi Oluwatimileyn

import csv
import os

def load_prices(filename):
    """
    Reads a CSV file and returns a dictionary of item prices.
    CSV format should be: item_name,price
    Example row: milk,3.99
    """
    prices = {}
    
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:  # Make sure row has both item and price
                    item = row[0].strip().lower()
                    try:
                        price = float(row[1].strip())
                        prices[item] = price
                    except ValueError:
                        # Skip rows where price isn't a valid number
                        continue
        return prices
    except FileNotFoundError:
        print(f"Warning: Could not find file '{filename}'")
        return {}
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}

def compare_item_price(store_a_prices, store_b_prices, item_name):
    """
    Compares price of a single item between two stores.
    Returns which store is cheaper or if item not found.
    """
    item = item_name.strip().lower()
    
    # Check if item exists in both stores
    in_a = item in store_a_prices
    in_b = item in store_b_prices
    
    if not in_a and not in_b:
        return "item not found in either store"
    elif not in_a:
        return f"only available at store B (${store_b_prices[item]:.2f})"
    elif not in_b:
        return f"only available at store A (${store_a_prices[item]:.2f})"
    
    price_a = store_a_prices[item]
    price_b = store_b_prices[item]
    
    if price_a < price_b:
        diff = price_b - price_a
        return f"store A is cheaper by ${diff:.2f}"
    elif price_b < price_a:
        diff = price_a - price_b
        return f"store B is cheaper by ${diff:.2f}"
    else:
        return "same price at both stores"

def calculate_list_total(store_prices, shopping_list):
    """
    Calculates total cost of shopping list at a specific store.
    Items not found are ignored with a warning.
    """
    total = 0.0
    missing_items = []
    
    for item in shopping_list:
        clean_item = item.strip().lower()
        if clean_item in store_prices:
            total += store_prices[clean_item]
        else:
            missing_items.append(item)
    
    # Print warnings for missing items
    if missing_items:
        print(f"  Note: Could not find: {', '.join(missing_items)}")
    
    return total

def find_cheaper_store(store_a_prices, store_b_prices, shopping_list):
    """
    Compares total cost of shopping list at both stores.
    Returns dictionary with totals, cheaper store, and savings amount.
    """
    total_a = calculate_list_total(store_a_prices, shopping_list)
    total_b = calculate_list_total(store_b_prices, shopping_list)
    
    if total_a < total_b:
        cheaper = "Store A"
        savings = total_b - total_a
    elif total_b < total_a:
        cheaper = "Store B"
        savings = total_a - total_b
    else:
        cheaper = "Tie - same total at both stores"
        savings = 0.0
    
    result = {
        "store_a_total": total_a,
        "store_b_total": total_b,
        "cheaper_store": cheaper,
        "savings": savings
    }
    
    return result

# Test functions
def test_load_prices_returns_correct_dictionary():
    """Test that load_prices correctly parses a CSV file."""
    # Create a test file
    test_data = "milk,3.99\nbread,2.50\neggs,4.25\n"
    test_filename = "test_prices_temp.csv"
    
    with open(test_filename, 'w') as f:
        f.write(test_data)
    
    result = load_prices(test_filename)
    
    # Check if dictionary has correct values
    assert result["milk"] == 3.99
    assert result["bread"] == 2.50
    assert result["eggs"] == 4.25
    assert len(result) == 3
    
    # Clean up
    os.remove(test_filename)
    print("✓ test_load_prices_returns_correct_dictionary passed")

def test_load_prices_handles_missing_file():
    """Test that load_prices handles non-existent files gracefully."""
    result = load_prices("this_file_does_not_exist_12345.csv")
    assert result == {}
    print("✓ test_load_prices_handles_missing_file passed")

def test_compare_item_price_store_a_cheaper():
    """Test compare_item_price when store A has better price."""
    store_a = {"milk": 2.99, "bread": 2.50}
    store_b = {"milk": 3.49, "bread": 2.50}
    
    result = compare_item_price(store_a, store_b, "milk")
    assert "store A is cheaper by $0.50" in result
    
    # Test tie
    result2 = compare_item_price(store_a, store_b, "bread")
    assert "same price" in result2
    
    print("✓ test_compare_item_price_store_a_cheaper passed")

def test_compare_item_price_item_not_found():
    """Test compare_item_price with items that don't exist."""
    store_a = {"milk": 2.99}
    store_b = {"eggs": 3.50}
    
    result = compare_item_price(store_a, store_b, "cereal")
    assert "not found in either store" in result
    
    result2 = compare_item_price(store_a, store_b, "eggs")
    assert "only available at store B" in result2
    
    print("✓ test_compare_item_price_item_not_found passed")

def test_calculate_list_total_with_empty_list():
    """Test calculate_list_total returns 0 for empty list."""
    store = {"milk": 3.99}
    result = calculate_list_total(store, [])
    assert result == 0.0
    print("✓ test_calculate_list_total_with_empty_list passed")

def test_calculate_list_total_with_missing_item_ignores_item():
    """Test that missing items are ignored in total calculation."""
    store = {"milk": 3.99, "bread": 2.50}
    shopping_list = ["milk", "cereal", "bread"]
    
    result = calculate_list_total(store, shopping_list)
    assert result == 6.49  # only milk and bread counted
    print("✓ test_calculate_list_total_with_missing_item_ignores_item passed")

def test_find_cheaper_store_calculates_savings_correctly():
    """Test that find_cheaper_store correctly identifies cheaper store."""
    store_a = {"milk": 2.99, "bread": 2.00, "eggs": 3.50}
    store_b = {"milk": 3.49, "bread": 1.50, "eggs": 4.00}
    shopping_list = ["milk", "bread", "eggs"]
    
    result = find_cheaper_store(store_a, store_b, shopping_list)
    
    # Store A total: 2.99 + 2.00 + 3.50 = 8.49
    # Store B total: 3.49 + 1.50 + 4.00 = 8.99
    # Store A should be cheaper by 0.50
    
    assert abs(result["store_a_total"] - 8.49) < 0.001
    assert abs(result["store_b_total"] - 8.99) < 0.001
    assert result["cheaper_store"] == "Store A"
    assert abs(result["savings"] - 0.50) < 0.001
    
    print("✓ test_find_cheaper_store_calculates_savings_correctly passed")

def run_all_tests():
    """Run all test functions."""
    print("\n--- Running Tests ---")
    test_load_prices_returns_correct_dictionary()
    test_load_prices_handles_missing_file()
    test_compare_item_price_store_a_cheaper()
    test_compare_item_price_item_not_found()
    test_calculate_list_total_with_empty_list()
    test_calculate_list_total_with_missing_item_ignores_item()
    test_find_cheaper_store_calculates_savings_correctly()
    print("--- All tests passed! ---\n")

def display_menu():
    """Shows the main menu options."""
    print("\n" + "="*50)
    print("        GROCERY BUDGET HELPER - MAIN MENU")
    print("="*50)
    print("1. Compare single item price between stores")
    print("2. Calculate total for a shopping list")
    print("3. Compare full shopping list between stores")
    print("4. Display store inventory")
    print("5. Run program tests")
    print("6. Exit")
    print("-"*50)

def display_inventory(store_prices, store_name):
    """Shows all items and prices for a store."""
    if not store_prices:
        print(f"\n{store_name} has no items loaded.")
        return
    
    print(f"\n{store_name} Inventory:")
    print("-"*30)
    for item, price in sorted(store_prices.items()):
        print(f"  {item:15} ${price:.2f}")

def get_shopping_list_from_user():
    """Gets a shopping list from user input."""
    print("\nEnter items one at a time (or 'done' to finish):")
    shopping_list = []
    
    while True:
        item = input("  Item: ").strip()
        if item.lower() == 'done':
            break
        elif item:
            shopping_list.append(item)
    
    return shopping_list

def main():
    """Main program function."""
    print("\nWelcome to Grocery Budget Helper!")
    print("This program helps you save money by comparing store prices.\n")
    
    # Load store data
    print("Loading store price data...")
    store_a_file = input("Enter filename for Store A (default: store_a.csv): ").strip()
    if not store_a_file:
        store_a_file = "store_a.csv"
    
    store_b_file = input("Enter filename for Store B (default: store_b.csv): ").strip()
    if not store_b_file:
        store_b_file = "store_b.csv"
    
    store_a_prices = load_prices(store_a_file)
    store_b_prices = load_prices(store_b_file)
    
    if not store_a_prices and not store_b_prices:
        print("\nNo price data loaded. Please create CSV files first.")
        print("CSV format: item_name,price")
        print("Example: milk,3.99")
        return
    
    print(f"\nLoaded {len(store_a_prices)} items from Store A")
    print(f"Loaded {len(store_b_prices)} items from Store B")
    
    # Main program loop
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            # Compare single item
            item = input("\nEnter item name to compare: ").strip()
            result = compare_item_price(store_a_prices, store_b_prices, item)
            print(f"\nResult: {result}")
            
        elif choice == '2':
            # Calculate total for one store
            store_choice = input("Which store? (A/B): ").upper().strip()
            shopping_list = get_shopping_list_from_user()
            
            if store_choice == 'A':
                total = calculate_list_total(store_a_prices, shopping_list)
                print(f"\nTotal at Store A: ${total:.2f}")
            elif store_choice == 'B':
                total = calculate_list_total(store_b_prices, shopping_list)
                print(f"\nTotal at Store B: ${total:.2f}")
            else:
                print("Invalid store choice.")
                
        elif choice == '3':
            # Compare full shopping list
            print("\nCreating shopping list to compare between stores...")
            shopping_list = get_shopping_list_from_user()
            
            if shopping_list:
                print("\nCalculating totals...")
                result = find_cheaper_store(store_a_prices, store_b_prices, shopping_list)
                
                print("\n" + "="*40)
                print("SHOPPING LIST COMPARISON RESULTS")
                print("="*40)
                print(f"Store A total: ${result['store_a_total']:.2f}")
                print(f"Store B total: ${result['store_b_total']:.2f}")
                print("-"*40)
                print(f"Cheaper option: {result['cheaper_store']}")
                if result['savings'] > 0:
                    print(f"You'll save: ${result['savings']:.2f}")
                print("="*40)
            else:
                print("No items entered.")
                
        elif choice == '4':
            # Display inventory
            print("\nWhich store inventory?")
            store_choice = input("(A/B/both): ").upper().strip()
            
            if store_choice in ['A', 'BOTH']:
                display_inventory(store_a_prices, "Store A")
            if store_choice in ['B', 'BOTH']:
                display_inventory(store_b_prices, "Store B")
                
        elif choice == '5':
            # Run tests
            run_all_tests()
            
        elif choice == '6':
            print("\nThanks for using Grocery Budget Helper. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please enter 1-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()