# 💰 Personal Expense Tracker

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#testing)
[![Code Style](https://img.shields.io/badge/code%20style-clean%20modular-orange.svg)](#project-structure)

A clean, modular, and robust command-line based **Personal Expense Tracker** built in Python. Designed to help users effortlessly record, categorize, analyze, and visualize their daily spending habits with persistent CSV file storage and interactive Matplotlib charts.

---

## 📌 Project Overview

Managing personal finances is essential for financial freedom and healthy spending habits. **Personal Expense Tracker** provides a complete CLI toolkit that enables users to:
1. **Record & Categorize Expenses**: Log expense amount, category (e.g., Food, Transport, Entertainment, Groceries, Utilities), and date.
2. **Tabulate Spending**: Display structured ASCII tables of all logged expenses with optional category filtering and sorting.
3. **Generate Analytics Reports**: Compute total expenditure, category-wise breakdowns, monthly spending trends, average transaction amounts, and identify the highest single expense.
4. **Visualize Spending Trends**: Generate publication-ready **Pie Charts** and **Bar Charts** powered by Matplotlib, showing category share and monthly trends.
5. **Persistent Storage**: Save and load records seamlessly from CSV files using Python's native `csv` module.
6. **Graceful Error Handling**: Input validation for non-numeric amounts, malformed dates, and edge cases using `try-except` blocks.

---

## 🚀 Key Features

* **Lists & Dictionaries Data Architecture**: All expense records are represented as dictionary objects (`{'amount': 50.0, 'category': 'Food', 'date': '2024-10-13'}`) maintained within dynamic lists.
* **CSV File Handling**: Automatically loads past records on startup and safely writes updates upon adding expenses or exiting.
* **Interactive CLI Menu**: Intuitive number-driven navigation powered by `while` loops and `if-elif-else` control flow.
* **Matplotlib Visualizations**:
  * 🥧 **Category Distribution (Pie Chart)**: Clear percentage breakdown of spending categories.
  * 📊 **Category-wise Spending (Bar Chart)**: Comparative spend across categories.
  * 📈 **Monthly Spending Trends (Bar Chart)**: Track spending progression over months.
  * 🖥️ **Analytics Dashboard**: Multi-panel visualization combining category and monthly breakdowns.
* **High Reliability**: Validates positive numeric amounts and standard `YYYY-MM-DD` date formats (defaults to today's date if left blank).
* **Automated CI/CD**: Includes automated GitHub Actions workflow verifying tests on Python 3.9 through 3.12.

---

## 📂 Project Structure

```text
personal-expense-tracker/
├── .github/
│   └── workflows/
│       └── python-app.yml       # GitHub Actions CI automated testing
├── data/
│   └── expenses.csv             # Persistent CSV storage file
├── reports/
│   └── .gitkeep                 # Directory where chart images are saved
├── src/
│   ├── __init__.py              # Package initializer
│   ├── tracker.py               # Core logic: add, view, calculations, reports
│   ├── storage.py               # CSV load & save handling
│   ├── visualizer.py            # Matplotlib charts & dashboard generation
│   └── utils.py                 # Input validation, formatting & ASCII tables
├── tests/
│   ├── __init__.py
│   └── test_tracker.py          # 13 comprehensive unit tests
├── .gitignore                   # Python gitignore configuration
├── LICENSE                      # MIT Open-Source License
├── main.py                      # Main application entry point & CLI loop
├── README.md                    # Project documentation
├── requirements.txt             # Project dependencies (matplotlib)
└── setup.py                     # Package setup script
```

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8 or higher installed on your machine.
* `git` (for version control and publishing to GitHub).

### 1. Clone or Open the Repository
```bash
git clone https://github.com/your-username/personal-expense-tracker.git
cd personal-expense-tracker
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎮 How to Run

### Option 1: Modern Interactive Web Application (Recommended)
Launch the web server:
```bash
python app.py
```
Then open your browser and navigate to:
👉 **`http://localhost:5000`**

### Option 2: Command-Line Interface (CLI)
Launch the CLI application:
```bash
python main.py
```

### Interactive Menu
Upon launch, you will be greeted with the main menu:

```text
==========================================
  Welcome to Personal Expense Tracker!   
==========================================
1. Add an Expense
2. View All Expenses
3. Generate Report
4. Visualize Expenses
5. Save and Exit
==========================================
Enter your choice:
```

---

## 📖 Usage Examples

### 1. Adding an Expense
```text
--- Add New Expense ---
Enter expense amount ($): 50.00
Enter category (e.g., Food, Transport, Entertainment): Food
Enter date (YYYY-MM-DD, default '2024-10-13'): 2024-10-13

[+] Successfully added: $50.00 for Food on 2024-10-13.
```

### 2. Viewing Expenses
```text
=============================================
EXPENSE LIST (11 items)
=============================================
Date        Category       Amount
----------  -------------  ------
2024-10-13  Food           $50.00
2024-10-12  Transport      $20.00
2024-10-10  Entertainment  $35.50
2024-10-08  Groceries      $85.20
2024-10-05  Utilities      $65.00
2024-10-01  Food           $28.75
2024-09-28  Transport      $22.00
2024-09-25  Entertainment  $45.00
2024-09-20  Groceries      $92.40
2024-09-15  Food           $34.10
2024-09-10  Utilities      $60.00
---------------------------------------------
Total: $537.95
=============================================
```

### 3. Generating a Summary Report
```text
=======================================================
           PERSONAL EXPENSE REPORT SUMMARY           
=======================================================
 Total Spent            : $537.95
 Total Transactions     : 11
 Average Transaction    : $48.90
 Highest Expense        : $92.40 (Groceries on 2024-09-20)
-------------------------------------------------------

--- SPENDING BY CATEGORY ---
Category       Total Spent  Share (%)
-------------  -----------  ---------
Groceries      $177.60       33.0%   
Utilities      $125.00       23.2%   
Food           $112.85       21.0%   
Entertainment  $80.50        15.0%   
Transport      $42.00         7.8%   

--- MONTHLY SPENDING BREAKDOWN ---
Month (YYYY-MM)  Total Spent  Share (%)
---------------  -----------  ---------
2024-09          $253.50       47.1%   
2024-10          $284.45       52.9%   
=======================================================
```

### 4. Data Visualization
Selecting option `4` opens chart options:
1. **Spending by Category (Pie Chart)**: Creates high-res pie chart showing percentage allocation per category.
2. **Spending by Category (Bar Chart)**: Generates comparative bars labeled with dollar values.
3. **Monthly Spending Trend (Bar Chart)**: Visualizes month-over-month expenditure changes.
4. **Comprehensive Dashboard**: Multi-panel visualization combining both views.

*(All generated charts are automatically saved under `reports/` for reporting and documentation).*

---

## 🧪 Testing

The project includes an automated test suite covering calculations, data handling, validation, and visualizations. Run tests with:

```bash
python -m unittest discover -s tests
```

Output:
```text
.............
----------------------------------------------------------------------
Ran 13 tests in 0.052s

OK
```

---

## 🌐 Publishing to GitHub (Step-by-Step)

To publish this project to GitHub as a public repository accessible to everyone:

### Step 1: Open Terminal in the Project Directory
```bash
cd "C:\Users\vinay\.gemini\antigravity\scratch\personal-expense-tracker"
```

### Step 2: Initialize Git and Commit
```bash
git init
git add .
git commit -m "feat: initial commit of personal expense tracker project"
```

### Step 3: Create a Public Repository on GitHub
1. Log in to [GitHub](https://github.com/).
2. Click the **+** icon in the top-right corner and select **New repository**.
3. Repository name: `personal-expense-tracker`
4. Description: `A command-line based Personal Expense Tracker with analytics and visualization`
5. Select **Public** so it is accessible by everyone.
6. Leave "Add a README file", ".gitignore", and "License" unchecked (we already have them).
7. Click **Create repository**.

### Step 4: Link and Push to GitHub
Run the following commands in your terminal:
```bash
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/personal-expense-tracker.git
git push -u origin main
```

Your project will now be live, public, and accessible to everyone on GitHub!

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details. It is free and open to everyone for study, modification, and distribution.
