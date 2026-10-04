"""
main.py - Entry Point for Personal Expense Tracker
A command-line based Personal Expense Tracker to help users record,
categorize, analyze, and visualize their daily expenses.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any

from src.storage import load_expenses, save_expenses
from src.tracker import (
    add_expense,
    view_expenses,
    generate_report,
)
from src.visualizer import (
    plot_category_pie,
    plot_category_bar,
    plot_monthly_bar,
    plot_spending_dashboard
)
from src.utils import (
    validate_amount,
    validate_date,
    validate_category,
    format_currency
)

# Default data file path
DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "expenses.csv")


def display_menu() -> None:
    """Displays the main command-line menu."""
    print("\n" + "=" * 42)
    print("  Welcome to Personal Expense Tracker!   ")
    print("=" * 42)
    print("1. Add an Expense")
    print("2. View All Expenses")
    print("3. Generate Report")
    print("4. Visualize Expenses")
    print("5. Save and Exit")
    print("=" * 42)


def handle_add_expense(expenses: List[Dict[str, Any]], filepath: str) -> None:
    """Handles user input and error handling for adding a new expense."""
    print("\n--- Add New Expense ---")

    # 1. Amount Input
    while True:
        try:
            amt_raw = input("Enter expense amount ($): ").strip()
            is_valid, amount, err_msg = validate_amount(amt_raw)
            if is_valid and amount is not None:
                break
            print(f"[!] Error: {err_msg}")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            return

    # 2. Category Input
    while True:
        try:
            cat_raw = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
            is_valid, category, err_msg = validate_category(cat_raw)
            if is_valid and category is not None:
                break
            print(f"[!] Error: {err_msg}")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            return

    # 3. Date Input
    today_default = datetime.now().strftime("%Y-%m-%d")
    while True:
        try:
            date_raw = input(f"Enter date (YYYY-MM-DD, default '{today_default}'): ").strip()
            is_valid, date_val, err_msg = validate_date(date_raw, allow_blank=True)
            if is_valid and date_val is not None:
                break
            print(f"[!] Error: {err_msg}")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            return

    # Add to list
    new_entry = add_expense(expenses, amount, category, date_val)
    print(f"\n[+] Successfully added: {format_currency(new_entry['amount'])} for {new_entry['category']} on {new_entry['date']}.")
    
    # Auto-save changes to CSV
    save_expenses(filepath, expenses)


def handle_view_expenses(expenses: List[Dict[str, Any]]) -> None:
    """Handles viewing expenses with optional category filtering."""
    if not expenses:
        print("\n[!] No expenses recorded yet. Use option 1 to add your first expense.")
        return

    print("\n--- View Expenses ---")
    cat_filter = input("Filter by category? (Leave blank to view all): ").strip()
    filter_val = cat_filter if cat_filter else None
    view_expenses(expenses, filter_category=filter_val)


def handle_visualizations(expenses: List[Dict[str, Any]]) -> None:
    """Handles data visualization sub-menu."""
    if not expenses:
        print("\n[!] No expenses to visualize. Please add some expenses first.")
        return

    while True:
        print("\n--- Data Visualization ---")
        print("1. Spending by Category (Pie Chart)")
        print("2. Spending by Category (Bar Chart)")
        print("3. Monthly Spending Trend (Bar Chart)")
        print("4. Comprehensive Dashboard (Pie & Bar)")
        print("5. Back to Main Menu")
        
        choice = input("Select a visualization option (1-5): ").strip()

        if choice == "1":
            print("\nGenerating Category Pie Chart...")
            plot_category_pie(expenses, show=True)
        elif choice == "2":
            print("\nGenerating Category Bar Chart...")
            plot_category_bar(expenses, show=True)
        elif choice == "3":
            print("\nGenerating Monthly Bar Chart...")
            plot_monthly_bar(expenses, show=True)
        elif choice == "4":
            print("\nGenerating Complete Dashboard...")
            plot_spending_dashboard(expenses, show=True)
        elif choice == "5":
            break
        else:
            print("[!] Invalid option. Please select 1, 2, 3, 4, or 5.")


def main(data_filepath: str = DEFAULT_DATA_FILE) -> None:
    """
    Main application loop.
    Implements control flow using while loops, for loops, and if-else branches.
    """
    print("Initializing Personal Expense Tracker...")
    expenses = load_expenses(data_filepath)
    print(f"Loaded {len(expenses)} expense(s) from '{os.path.basename(data_filepath)}'.")

    while True:
        display_menu()
        try:
            choice = input("Enter your choice: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting application. Saving data...")
            save_expenses(data_filepath, expenses)
            print("Goodbye!")
            break

        # Control flow using if-else statements
        if choice == "1":
            handle_add_expense(expenses, data_filepath)

        elif choice == "2":
            handle_view_expenses(expenses)

        elif choice == "3":
            generate_report(expenses)

        elif choice == "4":
            handle_visualizations(expenses)

        elif choice == "5":
            print("\nSaving expenses to file...")
            if save_expenses(data_filepath, expenses):
                print(f"[+] Successfully saved {len(expenses)} expense(s) to '{data_filepath}'.")
            else:
                print("[!] Error saving data.")
            print("Thank you for using Personal Expense Tracker. Goodbye!")
            break

        else:
            print("\n[!] Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    filepath_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATA_FILE
    main(filepath_arg)
