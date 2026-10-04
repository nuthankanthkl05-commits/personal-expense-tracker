"""
tracker.py - Core Expense Tracking Logic
Implements data structures (lists of dictionaries) and functions for managing,
viewing, categorizing, and calculating expense reports.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from src.utils import format_currency, print_table


def add_expense(
    expenses: List[Dict[str, Any]],
    amount: float,
    category: str,
    date: str
) -> Dict[str, Any]:
    """
    Adds a new expense dictionary to the expenses list.
    
    Args:
        expenses: The list of expense dictionaries.
        amount: Float expense amount.
        category: Category string (e.g., Food, Transport).
        date: Date string formatted as YYYY-MM-DD.
        
    Returns:
        The newly created expense dictionary.
    """
    expense = {
        "amount": round(float(amount), 2),
        "category": category.strip().title(),
        "date": date.strip()
    }
    expenses.append(expense)
    return expense


def view_expenses(
    expenses: List[Dict[str, Any]],
    filter_category: Optional[str] = None,
    sort_by: str = "date",
    reverse: bool = True
) -> None:
    """
    Displays all expenses in a clean, tabular format.
    Supports optional filtering by category and sorting by date or amount.
    
    Args:
        expenses: List of expense dictionaries.
        filter_category: Optional category name to filter by.
        sort_by: Field to sort by ('date', 'amount', 'category').
        reverse: Sort descending if True (default True for dates).
    """
    if not expenses:
        print("\n[!] No expenses recorded yet. Start by adding one!")
        return

    # Filter if category provided
    filtered = expenses
    if filter_category:
        filtered = [
            e for e in expenses
            if e["category"].lower() == filter_category.strip().lower()
        ]
        if not filtered:
            print(f"\n[!] No expenses found under category: '{filter_category}'.")
            return

    # Sort
    try:
        sorted_expenses = sorted(
            filtered,
            key=lambda x: x.get(sort_by, ""),
            reverse=reverse
        )
    except Exception:
        sorted_expenses = filtered

    print("\n" + "=" * 45)
    header_title = f"EXPENSE LIST ({len(sorted_expenses)} item{'s' if len(sorted_expenses) != 1 else ''})"
    if filter_category:
        header_title += f" [Category: {filter_category.title()}]"
    print(header_title)
    print("=" * 45)

    headers = ["Date", "Category", "Amount"]
    rows = [
        [e["date"], e["category"], format_currency(e["amount"])]
        for e in sorted_expenses
    ]

    print_table(headers, rows)
    
    # Show subtotal for current view
    subtotal = sum(e["amount"] for e in sorted_expenses)
    print("-" * 45)
    print(f"Total: {format_currency(subtotal)}")
    print("=" * 45 + "\n")


def calculate_total_spending(expenses: List[Dict[str, Any]]) -> float:
    """
    Calculates total spending across all expenses.
    """
    if not expenses:
        return 0.0
    return round(sum(e["amount"] for e in expenses), 2)


def calculate_spending_by_category(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Groups expenses and aggregates total spending per category.
    
    Returns:
        Dictionary mapping category names to total spent, sorted descending by total.
    """
    totals: Dict[str, float] = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = totals.get(cat, 0.0) + exp["amount"]
    
    # Sort by amount descending
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def calculate_monthly_spending(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Groups expenses by month (YYYY-MM) and calculates total spending.
    
    Returns:
        Dictionary mapping 'YYYY-MM' strings to total amounts, sorted chronologically.
    """
    monthly: Dict[str, float] = {}
    for exp in expenses:
        # Date is YYYY-MM-DD, month is first 7 chars
        month_key = exp["date"][:7] if len(exp["date"]) >= 7 else "Unknown"
        monthly[month_key] = monthly.get(month_key, 0.0) + exp["amount"]

    return dict(sorted(monthly.items(), key=lambda item: item[0]))


def calculate_weekly_spending(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Groups expenses by calendar week (YYYY-Www) and calculates total spending.
    
    Returns:
        Dictionary mapping week identifiers to total amounts, sorted chronologically.
    """
    weekly: Dict[str, float] = {}
    for exp in expenses:
        try:
            dt = datetime.strptime(exp["date"], "%Y-%m-%d")
            week_key = dt.strftime("%Y-W%U")
        except ValueError:
            week_key = "Unknown"
        weekly[week_key] = weekly.get(week_key, 0.0) + exp["amount"]

    return dict(sorted(weekly.items(), key=lambda item: item[0]))


def get_highest_expense(expenses: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Finds and returns the expense with the highest amount.
    """
    if not expenses:
        return None
    return max(expenses, key=lambda x: x["amount"])


def calculate_average_expense(expenses: List[Dict[str, Any]]) -> float:
    """
    Calculates the average amount per expense entry.
    """
    if not expenses:
        return 0.0
    return round(sum(e["amount"] for e in expenses) / len(expenses), 2)


def generate_report(expenses: List[Dict[str, Any]]) -> None:
    """
    Generates and prints a comprehensive textual expense report including:
    - Overall Total Spending
    - Number of Transactions
    - Average Spending per Transaction
    - Highest Single Expense
    - Spending Breakdown by Category (Amount and Percentage)
    - Spending Breakdown by Month
    """
    if not expenses:
        print("\n[!] No expenses to generate report from. Please add some expenses first.\n")
        return

    total = calculate_total_spending(expenses)
    count = len(expenses)
    avg = calculate_average_expense(expenses)
    highest = get_highest_expense(expenses)
    cat_totals = calculate_spending_by_category(expenses)
    monthly_totals = calculate_monthly_spending(expenses)

    print("\n" + "=" * 55)
    print("           PERSONAL EXPENSE REPORT SUMMARY           ")
    print("=" * 55)
    print(f" Total Spent            : {format_currency(total)}")
    print(f" Total Transactions     : {count}")
    print(f" Average Transaction    : {format_currency(avg)}")
    if highest:
        print(
            f" Highest Expense        : {format_currency(highest['amount'])} "
            f"({highest['category']} on {highest['date']})"
        )
    print("-" * 55)

    print("\n--- SPENDING BY CATEGORY ---")
    cat_headers = ["Category", "Total Spent", "Share (%)"]
    cat_rows = []
    for cat, cat_amt in cat_totals.items():
        percentage = (cat_amt / total * 100) if total > 0 else 0
        cat_rows.append([cat, format_currency(cat_amt), f"{percentage:5.1f}%"])
    print_table(cat_headers, cat_rows)

    print("\n--- MONTHLY SPENDING BREAKDOWN ---")
    month_headers = ["Month (YYYY-MM)", "Total Spent", "Share (%)"]
    month_rows = []
    for month, m_amt in monthly_totals.items():
        m_percent = (m_amt / total * 100) if total > 0 else 0
        month_rows.append([month, format_currency(m_amt), f"{m_percent:5.1f}%"])
    print_table(month_headers, month_rows)
    print("=" * 55 + "\n")
