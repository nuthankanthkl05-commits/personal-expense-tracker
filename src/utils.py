"""
utils.py - Utility and Validation Helpers
Provides input validation, currency formatting, and table printing for the CLI.
"""

from datetime import datetime
from typing import List, Optional, Tuple, Any


def validate_amount(amount_str: str) -> Tuple[bool, Optional[float], str]:
    """
    Validates that the provided amount string is a valid positive number.
    
    Args:
        amount_str: String input from user.
        
    Returns:
        (is_valid, parsed_float_or_None, error_message)
    """
    clean_str = amount_str.strip().replace("$", "")
    if not clean_str:
        return False, None, "Amount cannot be empty."

    try:
        val = float(clean_str)
        if val <= 0:
            return False, None, "Amount must be a positive number greater than 0."
        return True, round(val, 2), ""
    except ValueError:
        return False, None, f"Invalid number '{amount_str}'. Please enter a valid numerical amount (e.g., 25.50)."


def validate_date(date_str: str, allow_blank: bool = True) -> Tuple[bool, Optional[str], str]:
    """
    Validates that the provided date string matches YYYY-MM-DD format.
    If allow_blank is True and date_str is empty, defaults to today's date.
    
    Args:
        date_str: String input from user.
        allow_blank: If True, empty string defaults to current date.
        
    Returns:
        (is_valid, formatted_date_str, error_message)
    """
    clean_str = date_str.strip()
    if not clean_str:
        if allow_blank:
            today_str = datetime.now().strftime("%Y-%m-%d")
            return True, today_str, ""
        return False, None, "Date cannot be empty."

    try:
        parsed_dt = datetime.strptime(clean_str, "%Y-%m-%d")
        return True, parsed_dt.strftime("%Y-%m-%d"), ""
    except ValueError:
        return False, None, "Invalid date format. Please use YYYY-MM-DD (e.g., 2024-10-13)."


def validate_category(category_str: str) -> Tuple[bool, Optional[str], str]:
    """
    Validates and standardizes category names.
    
    Args:
        category_str: String input from user.
        
    Returns:
        (is_valid, title_cased_category, error_message)
    """
    clean_str = category_str.strip()
    if not clean_str:
        return False, None, "Category cannot be empty."
    if len(clean_str) > 30:
        return False, None, "Category name is too long (maximum 30 characters)."
    return True, clean_str.title(), ""


def format_currency(amount: float) -> str:
    """
    Formats a numeric amount as currency string, e.g. $50.00
    """
    return f"${amount:,.2f}"


def print_table(headers: List[str], rows: List[List[Any]]) -> None:
    """
    Prints a formatted, clean ASCII table matching the PDF example output.
    
    Example output format:
    Date       Category    Amount
    2024-10-13 Food        $50.00
    2024-10-12 Transport   $20.00
    """
    if not headers:
        return

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for idx, item in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(item)))

    # Format header
    header_line = "  ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
    separator = "  ".join("-" * col_widths[i] for i in range(len(headers)))

    print(header_line)
    print(separator)
    for row in rows:
        line = "  ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(row)))
        print(line)
