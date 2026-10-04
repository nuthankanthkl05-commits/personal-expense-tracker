"""
test_tracker.py - Comprehensive Unit Tests
Tests all core operations: addition, calculations, file handling, and validation.
"""

import os
import tempfile
import unittest
from datetime import datetime

from src.tracker import (
    add_expense,
    calculate_total_spending,
    calculate_spending_by_category,
    calculate_monthly_spending,
    get_highest_expense,
    calculate_average_expense
)
from src.storage import load_expenses, save_expenses
from src.utils import validate_amount, validate_date, validate_category


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        self.sample_expenses = [
            {"date": "2024-10-13", "category": "Food", "amount": 50.0},
            {"date": "2024-10-12", "category": "Transport", "amount": 20.0},
            {"date": "2024-09-15", "category": "Food", "amount": 30.0},
            {"date": "2024-09-10", "category": "Utilities", "amount": 100.0}
        ]

    def test_add_expense(self):
        expenses = []
        new_entry = add_expense(expenses, 45.5, "entertainment", "2024-10-14")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(new_entry["amount"], 45.5)
        self.assertEqual(new_entry["category"], "Entertainment")
        self.assertEqual(new_entry["date"], "2024-10-14")

    def test_calculate_total_spending(self):
        total = calculate_total_spending(self.sample_expenses)
        self.assertEqual(total, 200.0)

        # Empty test
        self.assertEqual(calculate_total_spending([]), 0.0)

    def test_calculate_spending_by_category(self):
        cat_data = calculate_spending_by_category(self.sample_expenses)
        self.assertEqual(cat_data["Food"], 80.0)
        self.assertEqual(cat_data["Transport"], 20.0)
        self.assertEqual(cat_data["Utilities"], 100.0)
        # Verify ordering (descending by total)
        top_category = list(cat_data.keys())[0]
        self.assertEqual(top_category, "Utilities")

    def test_calculate_monthly_spending(self):
        monthly = calculate_monthly_spending(self.sample_expenses)
        self.assertEqual(monthly["2024-10"], 70.0)
        self.assertEqual(monthly["2024-09"], 130.0)

    def test_get_highest_expense(self):
        highest = get_highest_expense(self.sample_expenses)
        self.assertIsNotNone(highest)
        self.assertEqual(highest["amount"], 100.0)
        self.assertEqual(highest["category"], "Utilities")

        self.assertIsNone(get_highest_expense([]))

    def test_calculate_average_expense(self):
        avg = calculate_average_expense(self.sample_expenses)
        self.assertEqual(avg, 50.0)
        self.assertEqual(calculate_average_expense([]), 0.0)

    def test_csv_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test_expenses.csv")
            
            # Save
            success = save_expenses(csv_path, self.sample_expenses)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(csv_path))

            # Load
            loaded = load_expenses(csv_path)
            self.assertEqual(len(loaded), 4)
            self.assertEqual(loaded[0]["category"], "Food")
            self.assertEqual(loaded[0]["amount"], 50.0)
            self.assertEqual(loaded[0]["date"], "2024-10-13")

    def test_amount_validation(self):
        # Valid
        valid, val, _ = validate_amount("50.00")
        self.assertTrue(valid)
        self.assertEqual(val, 50.0)

        valid, val, _ = validate_amount("$120.50")
        self.assertTrue(valid)
        self.assertEqual(val, 120.5)

        # Invalid
        valid, _, _ = validate_amount("-10")
        self.assertFalse(valid)

        valid, _, _ = validate_amount("abc")
        self.assertFalse(valid)

        valid, _, _ = validate_amount("")
        self.assertFalse(valid)

    def test_date_validation(self):
        # Valid explicit
        valid, dt, _ = validate_date("2024-10-13")
        self.assertTrue(valid)
        self.assertEqual(dt, "2024-10-13")

        # Blank date defaults to today
        today = datetime.now().strftime("%Y-%m-%d")
        valid, dt, _ = validate_date("", allow_blank=True)
        self.assertTrue(valid)
        self.assertEqual(dt, today)

        # Invalid formats
        valid, _, _ = validate_date("13-10-2024")
        self.assertFalse(valid)

        valid, _, _ = validate_date("invalid-date")
        self.assertFalse(valid)

    def test_category_validation(self):
        valid, cat, _ = validate_category("food")
        self.assertTrue(valid)
        self.assertEqual(cat, "Food")

        valid, _, _ = validate_category("   ")
        self.assertFalse(valid)

    def test_weekly_spending(self):
        from src.tracker import calculate_weekly_spending
        weekly = calculate_weekly_spending(self.sample_expenses)
        self.assertIsInstance(weekly, dict)
        self.assertTrue(len(weekly) > 0)

    def test_view_and_report_output(self):
        from src.tracker import view_expenses, generate_report
        # Test that calling these with data and with empty data does not raise exceptions
        view_expenses(self.sample_expenses)
        view_expenses(self.sample_expenses, filter_category="Food")
        view_expenses([])
        generate_report(self.sample_expenses)
        generate_report([])

    def test_visualizer_files(self):
        from src.visualizer import (
            plot_category_pie,
            plot_category_bar,
            plot_monthly_bar,
            plot_spending_dashboard
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            pie_path = os.path.join(tmpdir, "pie.png")
            bar_path = os.path.join(tmpdir, "bar.png")
            month_path = os.path.join(tmpdir, "month.png")
            dash_path = os.path.join(tmpdir, "dash.png")

            self.assertIsNotNone(plot_category_pie(self.sample_expenses, output_path=pie_path, show=False))
            self.assertTrue(os.path.exists(pie_path))

            self.assertIsNotNone(plot_category_bar(self.sample_expenses, output_path=bar_path, show=False))
            self.assertTrue(os.path.exists(bar_path))

            self.assertIsNotNone(plot_monthly_bar(self.sample_expenses, output_path=month_path, show=False))
            self.assertTrue(os.path.exists(month_path))

            self.assertIsNotNone(plot_spending_dashboard(self.sample_expenses, output_path=dash_path, show=False))
            self.assertTrue(os.path.exists(dash_path))


if __name__ == "__main__":
    unittest.main()

