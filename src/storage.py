"""
storage.py - File Handling Module
Handles saving and loading expense data to and from CSV files using Python's standard `csv` module.
"""

import csv
import os
from typing import List, Dict, Any

CSV_HEADER = ["date", "category", "amount"]


def load_expenses(filepath: str) -> List[Dict[str, Any]]:
    """
    Load expenses from a CSV file.
    Each row is converted into a dictionary with keys: 'date', 'category', 'amount'.
    
    Args:
        filepath: Path to the CSV file.
        
    Returns:
        List of expense dictionaries.
    """
    expenses: List[Dict[str, Any]] = []

    if not os.path.exists(filepath):
        # If the file does not exist, return an empty list
        return expenses

    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, start=2):
                try:
                    date = row.get("date", "").strip()
                    category = row.get("category", "").strip().capitalize()
                    amount_raw = row.get("amount", "").strip().replace("$", "")
                    
                    if not date or not category or not amount_raw:
                        continue
                    
                    amount = float(amount_raw)
                    expenses.append({
                        "date": date,
                        "category": category,
                        "amount": amount
                    })
                except (ValueError, TypeError) as e:
                    print(f"Warning: Skipping malformed row {row_num} in {filepath}: {row} ({e})")
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")

    return expenses


def save_expenses(filepath: str, expenses: List[Dict[str, Any]]) -> bool:
    """
    Save the list of expense dictionaries to a CSV file.
    
    Args:
        filepath: Path to the CSV file.
        expenses: List of expense dictionaries.
        
    Returns:
        True if successfully saved, False otherwise.
    """
    try:
        # Ensure parent directory exists
        dirname = os.path.dirname(filepath)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADER)
            writer.writeheader()
            for expense in expenses:
                writer.writerow({
                    "date": expense.get("date", ""),
                    "category": expense.get("category", ""),
                    "amount": f"{expense.get('amount', 0.0):.2f}"
                })
        return True
    except Exception as e:
        print(f"Error saving expenses to '{filepath}': {e}")
        return False
