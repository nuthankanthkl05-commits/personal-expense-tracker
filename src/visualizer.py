"""
visualizer.py - Data Visualization Module
Uses Matplotlib to generate pie charts and bar charts for category distribution
and monthly/weekly spending trends. Saves high-quality images and displays them.
"""

import os
from typing import List, Dict, Any, Optional
import matplotlib
matplotlib.use("Agg")  # Cloud-safe headless backend for servers and Render
import matplotlib.pyplot as plt
from src.tracker import (
    calculate_spending_by_category,
    calculate_monthly_spending,
    calculate_weekly_spending
)


def _ensure_dir(path: str) -> None:
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)


def plot_category_pie(
    expenses: List[Dict[str, Any]],
    output_path: Optional[str] = "reports/category_spending_pie.png",
    show: bool = True
) -> Optional[str]:
    """
    Generates a Pie Chart showing expense distribution across categories.
    """
    cat_data = calculate_spending_by_category(expenses)
    if not cat_data:
        print("[!] No expense data available to visualize.")
        return None

    categories = list(cat_data.keys())
    amounts = list(cat_data.values())

    plt.figure(figsize=(8, 6))
    colors = plt.cm.Set3(range(len(categories)))

    wedges, texts, autotexts = plt.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        textprops=dict(color="black", fontsize=10),
        wedgeprops=dict(edgecolor="white", linewidth=1.5)
    )

    for autotext in autotexts:
        autotext.set_fontweight("bold")

    plt.title("Expense Distribution by Category", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()

    saved_path = None
    if output_path:
        _ensure_dir(output_path)
        plt.savefig(output_path, dpi=300)
        saved_path = os.path.abspath(output_path)
        print(f"[+] Saved Category Pie Chart to: {saved_path}")
    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

    return saved_path


def plot_category_bar(
    expenses: List[Dict[str, Any]],
    output_path: Optional[str] = "reports/category_spending_bar.png",
    show: bool = True
) -> Optional[str]:
    """
    Generates a Bar Chart showing spending per category.
    """
    cat_data = calculate_spending_by_category(expenses)
    if not cat_data:
        print("[!] No expense data available to visualize.")
        return None

    categories = list(cat_data.keys())
    amounts = list(cat_data.values())

    plt.figure(figsize=(9, 5))
    bars = plt.bar(categories, amounts, color="#3498db", edgecolor="#2980b9", width=0.5)

    plt.title("Total Spending by Category", fontsize=14, fontweight="bold")
    plt.xlabel("Category", fontsize=11)
    plt.ylabel("Amount ($)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Add amount labels above each bar
    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"${height:,.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=9, fontweight="bold"
        )

    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

    saved_path = None
    if output_path:
        _ensure_dir(output_path)
        plt.savefig(output_path, dpi=300)
        saved_path = os.path.abspath(output_path)
        print(f"[+] Saved Category Bar Chart to: {saved_path}")

    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

    return saved_path


def plot_monthly_bar(
    expenses: List[Dict[str, Any]],
    output_path: Optional[str] = "reports/monthly_spending_bar.png",
    show: bool = True
) -> Optional[str]:
    """
    Generates a Bar Chart showing total monthly spending over time.
    """
    monthly_data = calculate_monthly_spending(expenses)
    if not monthly_data:
        print("[!] No expense data available to visualize.")
        return None

    months = list(monthly_data.keys())
    amounts = list(monthly_data.values())

    plt.figure(figsize=(9, 5))
    bars = plt.bar(months, amounts, color="#2ecc71", edgecolor="#27ae60", width=0.45)

    plt.title("Monthly Spending Overview", fontsize=14, fontweight="bold")
    plt.xlabel("Month (YYYY-MM)", fontsize=11)
    plt.ylabel("Total Spent ($)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"${height:,.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=9, fontweight="bold"
        )

    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()

    saved_path = None
    if output_path:
        _ensure_dir(output_path)
        plt.savefig(output_path, dpi=300)
        saved_path = os.path.abspath(output_path)
        print(f"[+] Saved Monthly Spending Chart to: {saved_path}")

    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

    return saved_path


def plot_spending_dashboard(
    expenses: List[Dict[str, Any]],
    output_path: Optional[str] = "reports/expense_dashboard.png",
    show: bool = True
) -> Optional[str]:
    """
    Generates a 2x1 Combined Dashboard containing:
    1. Category Distribution (Pie Chart)
    2. Monthly Spending (Bar Chart)
    """
    if not expenses:
        print("[!] No expense data available to visualize.")
        return None

    cat_data = calculate_spending_by_category(expenses)
    monthly_data = calculate_monthly_spending(expenses)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Subplot 1: Pie chart
    ax1.pie(
        list(cat_data.values()),
        labels=list(cat_data.keys()),
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Pastel1(range(len(cat_data))),
        wedgeprops=dict(edgecolor="white", linewidth=1.2)
    )
    ax1.set_title("Spending by Category", fontsize=13, fontweight="bold")

    # Subplot 2: Monthly bar chart
    bars = ax2.bar(
        list(monthly_data.keys()),
        list(monthly_data.values()),
        color="#e67e22",
        edgecolor="#d35400",
        width=0.4
    )
    ax2.set_title("Monthly Spending", fontsize=13, fontweight="bold")
    ax2.set_xlabel("Month (YYYY-MM)", fontsize=10)
    ax2.set_ylabel("Total Spent ($)", fontsize=10)
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        h = bar.get_height()
        ax2.annotate(
            f"${h:,.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=8, fontweight="bold"
        )

    plt.suptitle("Personal Expense Tracker - Analytics Dashboard", fontsize=15, fontweight="bold")
    plt.tight_layout()

    saved_path = None
    if output_path:
        _ensure_dir(output_path)
        plt.savefig(output_path, dpi=300)
        saved_path = os.path.abspath(output_path)
        print(f"[+] Saved Comprehensive Dashboard to: {saved_path}")

    if show:
        try:
            plt.show()
        except Exception:
            pass
    plt.close()

    return saved_path
