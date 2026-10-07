# The Developers Arena — Week 4: File Handling & Final Project

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Completed%20(100%25)-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/Tests-23%2F23%20Passing-success.svg)](#)
[![Course](https://img.shields.io/badge/Developer's%20Arena-Week%204%20Final%20Project-orange.svg)](#)

**Course**: The Developers Arena  
**Module**: Week 4: File Handling & Final Project  
**Due Date**: October 7, 2026 (Overdue!)  
**Project**: Personal Finance Tracker  

---

## 📚 Theory Concepts

* **File Operations**: Reading from and writing to different file types
* **Text Files**: Working with `.txt` files for simple data storage
* **CSV Files**: Handling comma-separated values for structured data
* **Error Handling**: Managing file-related errors gracefully
* **Context Managers**: Using `'with'` statement for proper resource management
* **Code Organization**: Structuring projects into multiple files and modules
* **Debugging Techniques**: Advanced debugging for file operations

---

## 🛠️ Hands-On Practice (Completed)

All 5 standalone hands-on practice modules have been implemented, tested, and placed in the [`hands_on_practice/`](hands_on_practice/) folder:

| Module Script | Description | Execution Command |
| :--- | :--- | :--- |
| [`1_save_user_data.py`](hands_on_practice/1_save_user_data.py) | Saves user profile data to text file using context managers | `python hands_on_practice/1_save_user_data.py` |
| [`2_diary_notes.py`](hands_on_practice/2_diary_notes.py) | Notes & diary app with timestamped storage and search | `python hands_on_practice/2_diary_notes.py` |
| [`3_csv_processor.py`](hands_on_practice/3_csv_processor.py) | Reads, processes, and exports aggregated student grade CSV data | `python hands_on_practice/3_csv_processor.py` |
| [`4_quiz_game.py`](hands_on_practice/4_quiz_game.py) | File-handling quiz game persisting scores & high-score leaderboard | `python hands_on_practice/4_quiz_game.py` |
| [`5_persistent_todo.py`](hands_on_practice/5_persistent_todo.py) | Persistent CRUD To-Do task manager surviving program restarts | `python hands_on_practice/5_persistent_todo.py` |

- [x] Create a program that saves user data to a text file
- [x] Build a simple diary/notes application with file storage
- [x] Read and process data from CSV files
- [x] Create a quiz game that saves scores to a file
- [x] Build a to-do list that persists between program runs
- [x] Practice handling different file-related errors
- [x] Organize code into multiple modules

---

## 🎯 Project: Personal Finance Tracker

Build a complete personal finance tracker that allows users to add expenses, categorize them, save data to files, and generate monthly reports. This final project combines all concepts from Weeks 1-4 into a practical, real-world application.

---

## 🛠️ Technical Requirements

* Implement file operations for data persistence (JSON/CSV)
* Create a modular code structure with separate modules
* Add comprehensive error handling for file operations
* Implement data validation for all inputs
* Generate reports with statistics and visualizations
* Support multiple expense categories
* Add search and filter functionality
* Create a user-friendly menu system
* Implement backup and data recovery features

---

## 📋 Step-by-Step Guide

### Step 1: Project Architecture
* Create main project folder with subfolders for modules
* Design data structure for expenses
* Plan file formats for data storage
* Create module structure: `main.py`, `expenses.py`, `file_handler.py`, `reports.py`

### Step 2: Core Data Module
* Create `Expense` class with attributes (`date`, `amount`, `category`, `description`)
* Add validation methods for expense data
* Create `ExpenseManager` class to handle collections of expenses
* Implement methods to add, remove, and search expenses

### Step 3: File Handling Module
* Create functions to save/load expenses to JSON file
* Implement backup functionality
* Add CSV export/import features
* Handle file errors (missing files, permission errors, etc.)

### Step 4: Reports Module
* Create monthly summary reports
* Generate category-wise expense breakdown
* Add expense trend analysis
* Create basic text-based visualizations

### Step 5: Main Application
* Build user-friendly menu system
* Integrate all modules
* Add data validation at user interface level
* Implement search and filter functionality

### Step 6: Advanced Features
* Add budget setting and tracking
* Implement recurring expenses
* Add expense prediction based on history
* Create data export to multiple formats

### Step 7: Testing & Polish
* Test all file operations with edge cases
* Verify data persistence between runs
* Test error handling scenarios
* Add documentation and help system

---

## 💻 Sample Code

```python
# finance_tracker/main.py - Simplified version

class FinanceTracker:
    def __init__(self):
        self.expenses = []

    def run(self):
        print("=" * 60)
        print("          PERSONAL FINANCE TRACKER")
        print("=" * 60)

        while True:
            print("\n" + "=" * 40)
            print("            MAIN MENU")
            print("=" * 40)
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Search Expenses")
            print("4. Generate Monthly Report")
            print("5. View Category Breakdown")
            print("6. Set/Update Budget")
            print("7. Export Data to CSV")
            print("8. View Statistics")
            print("9. Backup/Restore Data")
            print("0. Exit")
            print("=" * 40)

            choice = input("\nEnter your choice (0-9): ").strip()

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.search_expenses()
            elif choice == '4':
                self.generate_monthly_report()
            elif choice == '5':
                self.view_category_breakdown()
            elif choice == '6':
                self.set_budget()
            elif choice == '7':
                self.export_data()
            elif choice == '8':
                self.view_statistics()
            elif choice == '9':
                self.backup_restore()
            elif choice == '0':
                print("\n" + "=" * 60)
                print("Thank you for using Personal Finance Tracker!")
                print("=" * 60)
                break
            else:
                print("Invalid choice! Please enter 0-9.")

    def add_expense(self):
        print("\n--- ADD NEW EXPENSE ---")
        # Implementation would go here
        print("Expense added successfully!")

    def view_expenses(self):
        print("\n--- ALL EXPENSES ---")
        # Implementation would go here
        print("Displaying all expenses...")

    def search_expenses(self):
        print("\n--- SEARCH EXPENSES ---")
        # Implementation would go here
        print("Searching expenses...")

    def generate_monthly_report(self):
        print("\n--- MONTHLY REPORT ---")
        # Implementation would go here
        print("Generating monthly report...")

    def view_category_breakdown(self):
        print("\n--- CATEGORY BREAKDOWN ---")
        # Implementation would go here
        print("Showing category breakdown...")

    def set_budget(self):
        print("\n--- SET/UPDATE BUDGET ---")
        # Implementation would go here
        print("Setting budget...")

    def export_data(self):
        print("\n--- EXPORT DATA ---")
        # Implementation would go here
        print("Exporting data...")

    def view_statistics(self):
        print("\n--- STATISTICS ---")
        # Implementation would go here
        print("Showing statistics...")

    def backup_restore(self):
        print("\n--- BACKUP/RESTORE ---")
        # Implementation would go here
        print("Managing backups...")

def main():
    tracker = FinanceTracker()
    tracker.run()

if __name__ == "__main__":
    main()
```

---

## 📊 Sample Output

```text
============================================================
                  PERSONAL FINANCE TRACKER
============================================================

========================================
               MAIN MENU
========================================
1. Add New Expense
2. View All Expenses
3. Search Expenses
4. Generate Monthly Report
5. View Category Breakdown
6. Set/Update Budget
7. Export Data to CSV
8. View Statistics
9. Backup/Restore Data
0. Exit
========================================

Enter your choice (0-9): 1

--- ADD NEW EXPENSE ---
Expense added successfully!

========================================
               MAIN MENU
========================================
...

Enter your choice (0-9): 0

============================================================
Thank you for using Personal Finance Tracker!
============================================================
```

---

## 🎂 Submission Requirements

### GitHub Structure:
```text
week4-finance-tracker/
├── finance_tracker/
│   ├── __init__.py
│   ├── main.py
│   ├── expense.py
│   ├── expense_manager.py
│   ├── file_handler.py
│   ├── reports.py
│   └── utils.py
├── data/
│   ├── expenses.json
│   ├── backup/
│   └── exports/
├── tests/
│   ├── test_expense.py
│   ├── test_file_handler.py
│   └── test_reports.py
├── requirements.txt
├── README.md
├── .gitignore
└── run.py
```

---

## 🏗️ Architecture & Implemented Modules

### 1. `finance_tracker/expense.py`
- `Expense` model with attributes: `id`, `date`, `amount`, `category`, `description`, `is_recurring`, `created_at`.
- Validation methods:
  - `validate_date`: Enforces strict `YYYY-MM-DD` calendar validity.
  - `validate_amount`: Ensures non-zero, positive numeric value.
  - `validate_category`: Ensures non-empty strings.
  - `validate_description`: Sanitizes text content.
- Serialization methods: `to_dict()` and `from_dict()`.

### 2. `finance_tracker/expense_manager.py`
- `ExpenseManager` collection handling.
- Adding, deleting by ID, searching, and filtering by keyword, date range, category, or amount.
- Budget management: sets and retrieves monthly spending limits.
- Recurring expense tracking.

### 3. `finance_tracker/file_handler.py`
- Safe atomic persistence to `data/expenses.json` using context managers (`with` statements).
- Error handling: Gracefully handles `FileNotFoundError`, `PermissionError`, and `json.JSONDecodeError`.
- Auto-quarantines corrupted JSON files with timestamped extensions.
- Automated & on-demand timestamped backups stored in `data/backup/`.
- Full backup listing and restoration with pre-restore safety snapshots.
- CSV export & import in `data/exports/` using `csv.DictWriter` and `csv.DictReader` with row-level error reporting.
- Formatted TXT report export.

### 4. `finance_tracker/reports.py`
- `ReportGenerator` computing:
  - Monthly summaries with transaction totals, daily spend averages, highest/lowest transactions.
  - Budget tracking with 80% consumption warnings and over-budget alerts.
  - Category breakdown with percentages and text-based ASCII visual bars (`[#####-----]`).
  - Historical spending trend analysis.
  - Heuristic month-end run-rate projection.

### 5. `finance_tracker/utils.py`
- Date formatting and validation.
- Currency display formatting.
- Cross-platform ASCII progress bar renderer.
- CLI input sanitizers (`prompt_date`, `prompt_float`, `prompt_non_empty`, `prompt_choice`).

### 6. `finance_tracker/main.py` & `run.py`
- Full interactive controller implementing options `0` through `9`.
- Input validation and feedback matching the specifications.

---

## 🧪 Automated Test Suite (23/23 Passing)

The project includes unit tests covering all modules and edge cases:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Coverage Summary:
- **`tests/test_expense.py`**: Validates creation, invalid dates, negative amounts, empty categories, dictionary serialization, adding/deleting, searching, and monthly filtering.
- **`tests/test_file_handler.py`**: Validates JSON save/load, missing file creation, corrupt JSON quarantine recovery, backup creation, backup restoration, CSV export/import, and malformed CSV row handling.
- **`tests/test_reports.py`**: Validates monthly totals, budget calculations, category percentages, ASCII bars, historical trends, and month-end projections.

```text
Ran 23 tests in 0.113s — OK
```

---

## 🚀 Execution Instructions

### Setup & Run
1. Clone or open the repository:
   ```bash
   cd week4-finance-tracker
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python run.py
   ```
4. Run automated test suite:
   ```bash
   python -m unittest discover -s tests -p "test_*.py"
   ```
