"""
app.py - Web Server Application for Personal Expense Tracker
Provides an interactive modern web UI, REST API, and data visualization endpoints
integrating directly with src/tracker.py, src/storage.py, and src/visualizer.py.
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from src.storage import load_expenses, save_expenses
from src.tracker import (
    add_expense,
    calculate_total_spending,
    calculate_spending_by_category,
    calculate_monthly_spending,
    get_highest_expense,
    calculate_average_expense
)
from src.visualizer import (
    plot_category_pie,
    plot_category_bar,
    plot_monthly_bar,
    plot_spending_dashboard
)
from src.utils import validate_amount, validate_date, validate_category

app = Flask(__name__)

# Data storage path
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "expenses.csv")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def get_analytics_summary(expenses):
    """Calculates all key metrics from the current expense list."""
    total = calculate_total_spending(expenses)
    count = len(expenses)
    avg = calculate_average_expense(expenses)
    highest = get_highest_expense(expenses)
    cat_spending = calculate_spending_by_category(expenses)
    month_spending = calculate_monthly_spending(expenses)

    return {
        "total": total,
        "count": count,
        "average": avg,
        "highest": highest,
        "category_spending": cat_spending,
        "monthly_spending": month_spending
    }


@app.route("/")
def home():
    """Renders the main web interface."""
    return render_template("index.html")


@app.route("/api/expenses", methods=["GET"])
def get_expenses_api():
    """Returns the current list of expenses and calculated metrics."""
    expenses = load_expenses(DATA_FILE)
    summary = get_analytics_summary(expenses)
    return jsonify({
        "success": True,
        "expenses": expenses,
        "reports": summary
    })


@app.route("/api/expenses", methods=["POST"])
def add_expense_api():
    """Adds a new expense and saves it to CSV."""
    data = request.get_json() or {}
    
    amount_raw = str(data.get("amount", ""))
    category_raw = str(data.get("category", ""))
    date_raw = str(data.get("date", ""))

    val_ok, amount, amt_err = validate_amount(amount_raw)
    if not val_ok:
        return jsonify({"success": False, "error": amt_err}), 400

    cat_ok, category, cat_err = validate_category(category_raw)
    if not cat_ok:
        return jsonify({"success": False, "error": cat_err}), 400

    date_ok, date_val, date_err = validate_date(date_raw, allow_blank=True)
    if not date_ok:
        return jsonify({"success": False, "error": date_err}), 400

    expenses = load_expenses(DATA_FILE)
    new_entry = add_expense(expenses, amount, category, date_val)
    save_expenses(DATA_FILE, expenses)

    return jsonify({
        "success": True,
        "expense": new_entry,
        "message": "Expense saved successfully."
    })


@app.route("/api/expenses/<int:index>", methods=["DELETE"])
def delete_expense_api(index):
    """Deletes an expense by its zero-based index and saves changes to CSV."""
    expenses = load_expenses(DATA_FILE)
    if index < 0 or index >= len(expenses):
        return jsonify({"success": False, "error": "Invalid index."}), 404

    removed = expenses.pop(index)
    save_expenses(DATA_FILE, expenses)

    return jsonify({
        "success": True,
        "removed": removed,
        "message": "Expense deleted."
    })


@app.route("/api/export-csv", methods=["GET"])
def export_csv():
    """Allows users to download the current CSV file."""
    if not os.path.exists(DATA_FILE):
        return "No data file found", 404
    return send_file(DATA_FILE, as_attachment=True, download_name="expenses.csv")


@app.route("/api/charts/category", methods=["GET"])
def get_category_chart():
    """Generates and serves the Matplotlib Category Pie Chart."""
    expenses = load_expenses(DATA_FILE)
    output_path = os.path.join(REPORTS_DIR, "web_category_pie.png")
    plot_category_pie(expenses, output_path=output_path, show=False)
    return send_file(output_path, mimetype="image/png")


@app.route("/api/charts/monthly", methods=["GET"])
def get_monthly_chart():
    """Generates and serves the Matplotlib Monthly Spending Bar Chart."""
    expenses = load_expenses(DATA_FILE)
    output_path = os.path.join(REPORTS_DIR, "web_monthly_bar.png")
    plot_monthly_bar(expenses, output_path=output_path, show=False)
    return send_file(output_path, mimetype="image/png")


@app.route("/api/charts/dashboard", methods=["GET"])
def get_dashboard_chart():
    """Generates and serves the comprehensive Matplotlib Dashboard."""
    expenses = load_expenses(DATA_FILE)
    output_path = os.path.join(REPORTS_DIR, "web_dashboard.png")
    plot_spending_dashboard(expenses, output_path=output_path, show=False)
    return send_file(output_path, mimetype="image/png")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Starting Personal Expense Tracker Web Server on port {port} ...")
    app.run(host="0.0.0.0", port=port, debug=False)

