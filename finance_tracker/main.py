import sys
import os
from datetime import datetime
from typing import Optional

from .expense import Expense, DEFAULT_CATEGORIES
from .expense_manager import ExpenseManager
from .file_handler import FileHandler
from .reports import ReportGenerator
from .utils import (
    format_currency,
    render_ascii_bar,
    prompt_date,
    prompt_float,
    prompt_non_empty,
    get_today_str
)

class FinanceTracker:
    def __init__(self, base_dir: Optional[str] = None):
        self.file_handler = FileHandler(base_dir=base_dir)
        self.manager = ExpenseManager()
        self.load_data()

    @property
    def expenses(self):
        return self.manager.expenses

    def load_data(self) -> None:
        data = self.file_handler.load_from_json()
        self.manager.load_from_dict(data)

    def save_data(self) -> bool:
        data = self.manager.to_dict()
        return self.file_handler.save_to_json(data)

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

            try:
                choice = input("\nEnter your choice (0-9): ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting application...")
                choice = '0'

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
        try:
            date_str = prompt_date("Enter date")

            print("\nSelect a Category:")
            for i, cat in enumerate(DEFAULT_CATEGORIES, start=1):
                print(f"  {i}. {cat}")
            print("  0. Custom Category")

            cat_choice = input(f"Choose category (0-{len(DEFAULT_CATEGORIES)}) [1]: ").strip()
            if cat_choice == "0":
                category = prompt_non_empty("Enter custom category name")
            elif cat_choice.isdigit() and 1 <= int(cat_choice) <= len(DEFAULT_CATEGORIES):
                category = DEFAULT_CATEGORIES[int(cat_choice) - 1]
            else:
                category = DEFAULT_CATEGORIES[0]

            amount = prompt_float("Enter amount")
            description = prompt_non_empty("Enter description")

            rec_in = input("Is this a recurring expense? (y/N): ").strip().lower()
            is_recurring = rec_in in ("y", "yes", "true", "1")

            expense = Expense(
                date=date_str,
                amount=amount,
                category=category,
                description=description,
                is_recurring=is_recurring
            )
            self.manager.add_expense(expense)
            self.save_data()

            print("Expense added successfully!")

            month_key = date_str[:7]
            budget = self.manager.get_budget(month_key)
            if budget and budget > 0:
                month_exps = self.manager.get_expenses_by_month(int(date_str[:4]), int(date_str[5:7]))
                spent = sum(e.amount for e in month_exps)
                if spent > budget:
                    print(f"[ALERT] Warning: You have exceeded your {month_key} budget of {format_currency(budget)}! (Spent: {format_currency(spent)})")
                elif spent >= 0.8 * budget:
                    print(f"[NOTICE] You have used {(spent/budget)*100:.1f}% of your {month_key} budget.")

        except (KeyboardInterrupt, EOFError):
            print("\nAdd expense cancelled.")
        except Exception as e:
            print(f"Error adding expense: {e}")

    def view_expenses(self):
        print("\n--- ALL EXPENSES ---")
        all_exps = self.manager.get_all_expenses(sort_by="date", reverse=True)
        if not all_exps:
            print("No expenses recorded yet. Choose option 1 to add your first expense.")
            return

        print(f"Total Records: {len(all_exps)} | Overall Spending: {format_currency(self.manager.get_total_expenses())}")
        print("-" * 75)
        print(f"{'ID':<8} {'Date':<12} {'Category':<20} {'Amount':>10}  {'Description':<20}")
        print("-" * 75)
        for exp in all_exps:
            rec_tag = " *" if exp.is_recurring else ""
            desc = exp.description[:18] + ".." if len(exp.description) > 20 else exp.description
            print(f"{exp.id:<8} {exp.date:<12} {exp.category[:19]:<20} {format_currency(exp.amount):>10}  {desc}{rec_tag}")
        print("-" * 75)
        print("(* indicates recurring expense)")

    def search_expenses(self):
        print("\n--- SEARCH EXPENSES ---")
        if not self.manager.expenses:
            print("No expenses available to search.")
            return

        print("Search options (Press Enter to skip any criteria):")
        kw = input("Keyword (searches description, category, ID): ").strip()
        cat = input("Category name: ").strip()
        start = input("Start date (YYYY-MM-DD): ").strip()
        end = input("End date (YYYY-MM-DD): ").strip()
        min_amt_str = input("Minimum amount: ").strip()
        max_amt_str = input("Maximum amount: ").strip()

        min_amt = float(min_amt_str) if min_amt_str else None
        max_amt = float(max_amt_str) if max_amt_str else None

        results = self.manager.search_expenses(
            keyword=kw if kw else None,
            category=cat if cat else None,
            start_date=start if start else None,
            end_date=end if end else None,
            min_amount=min_amt,
            max_amount=max_amt
        )

        print(f"\nFound {len(results)} matching expense(s):")
        if not results:
            print("No matching expenses found.")
            return

        print("-" * 75)
        print(f"{'ID':<8} {'Date':<12} {'Category':<20} {'Amount':>10}  {'Description':<20}")
        print("-" * 75)
        for exp in results:
            rec_tag = " *" if exp.is_recurring else ""
            desc = exp.description[:18] + ".." if len(exp.description) > 20 else exp.description
            print(f"{exp.id:<8} {exp.date:<12} {exp.category[:19]:<20} {format_currency(exp.amount):>10}  {desc}{rec_tag}")
        print("-" * 75)
        total_matched = sum(e.amount for e in results)
        print(f"Total of matched records: {format_currency(total_matched)}")

        del_choice = input("\nDo you want to delete any expense from these results? (Enter ID or press Enter to skip): ").strip()
        if del_choice:
            if self.manager.remove_expense(del_choice):
                self.save_data()
                print(f"Expense '{del_choice}' deleted successfully.")
            else:
                print(f"Expense ID '{del_choice}' not found.")

    def generate_monthly_report(self):
        print("\n--- MONTHLY REPORT ---")
        now = datetime.now()
        year_str = input(f"Enter year [Default: {now.year}]: ").strip()
        month_str = input(f"Enter month (1-12) [Default: {now.month}]: ").strip()

        year = int(year_str) if year_str.isdigit() else now.year
        month = int(month_str) if month_str.isdigit() and 1 <= int(month_str) <= 12 else now.month

        month_key = f"{year:04d}-{month:02d}"
        budget = self.manager.get_budget(month_key)

        summary = ReportGenerator.generate_monthly_summary(
            self.manager.expenses,
            year=year,
            month=month,
            budget=budget
        )

        report_text = ReportGenerator.format_monthly_report_text(summary)
        print("\n" + report_text)

        save_opt = input("\nExport this report to a text file? (y/N): ").strip().lower()
        if save_opt in ("y", "yes"):
            saved_path = self.file_handler.export_text_report(report_text, filename_prefix=f"report_{month_key}")
            if saved_path:
                print(f"Report exported to: {saved_path}")

    def view_category_breakdown(self):
        print("\n--- CATEGORY BREAKDOWN ---")
        breakdown = ReportGenerator.generate_category_breakdown(self.manager.expenses)
        if not breakdown:
            print("No expenses recorded to calculate breakdown.")
            return

        total_spent = self.manager.get_total_expenses()
        print(f"Total Cumulative Expenditure: {format_currency(total_spent)}\n")
        print(f"{'Category':<24} {'Count':>6} {'Amount':>12} {'Share (%)':>10}  {'Visual Breakdown':<25}")
        print("-" * 80)
        for item in breakdown:
            print(f"{item['category']:<24} {item['count']:>6} {format_currency(item['amount']):>12} {item['percentage']:>9.1f}%  {item['bar']}")
        print("-" * 80)

    def set_budget(self):
        print("\n--- SET/UPDATE BUDGET ---")
        now = datetime.now()
        default_month = f"{now.year:04d}-{now.month:02d}"
        month_key = input(f"Enter month (YYYY-MM) [Default: {default_month}]: ").strip()
        if not month_key:
            month_key = default_month

        current_budget = self.manager.get_budget(month_key)
        if current_budget is not None:
            print(f"Current overall budget for {month_key} is {format_currency(current_budget)}.")

        amt = prompt_float(f"Enter new overall budget amount for {month_key}")
        self.manager.set_budget(month_key, amt)
        self.save_data()
        print(f"Budget for {month_key} successfully set to {format_currency(amt)}!")

    def export_data(self):
        print("\n--- EXPORT DATA ---")
        if not self.manager.expenses:
            print("No expenses recorded to export.")
            return

        custom_name = input("Enter export CSV filename [Default: auto-generated]: ").strip()
        saved_path = self.file_handler.export_to_csv(
            self.manager.expenses,
            custom_filename=custom_name if custom_name else None
        )
        if saved_path:
            print(f"Successfully exported {len(self.manager.expenses)} records to:")
            print(f"  {saved_path}")

    def view_statistics(self):
        print("\n--- STATISTICS ---")
        if not self.manager.expenses:
            print("No expenses recorded yet to show statistics.")
            return

        all_exps = self.manager.expenses
        total = self.manager.get_total_expenses()
        avg = round(total / len(all_exps), 2)
        highest = max(all_exps, key=lambda x: x.amount)
        lowest = min(all_exps, key=lambda x: x.amount)

        print(f"Total Transactions : {len(all_exps)}")
        print(f"Total Spending     : {format_currency(total)}")
        print(f"Average / Expense  : {format_currency(avg)}")
        print(f"Highest Expense    : {format_currency(highest.amount)} on {highest.date} ({highest.category} - {highest.description})")
        print(f"Lowest Expense     : {format_currency(lowest.amount)} on {lowest.date} ({lowest.category} - {lowest.description})")

        print("\nSPENDING TREND (Recent Months):")
        trends = ReportGenerator.generate_trend_analysis(all_exps, max_months=6)
        if trends:
            for t in trends:
                chg_str = f"({'+' if t['change_percentage'] > 0 else ''}{t['change_percentage']}%)" if t['change_percentage'] is not None else ""
                print(f"  {t['month_key']} : {format_currency(t['amount']):>10}  {t['bar']} {chg_str}")
        else:
            print("  Insufficient monthly history for trend analysis.")

        now = datetime.now()
        pred = ReportGenerator.predict_month_end(all_exps, now.year, now.month)
        print(f"\nCURRENT MONTH RUN-RATE PREDICTION ({now.strftime('%B %Y')}):")
        print(f"  Spent so far     : {format_currency(pred['total_so_far'])} ({pred['days_elapsed']}/{pred['total_days']} days)")
        print(f"  Daily burn rate  : {format_currency(pred['daily_run_rate'])} / day")
        print(f"  Projected Total  : {format_currency(pred['projected_total'])}")

    def backup_restore(self):
        print("\n--- BACKUP/RESTORE ---")
        print("1. Create New Backup Now")
        print("2. List Available Backups")
        print("3. Restore from a Backup")
        print("0. Return to Main Menu")

        opt = input("\nSelect backup action (0-3): ").strip()
        if opt == "1":
            label = input("Enter optional label for backup (e.g. 'before_cleanup'): ").strip()
            path = self.file_handler.create_backup(custom_label=label if label else None)
            if path:
                print(f"Backup created successfully at:\n  {path}")
        elif opt == "2":
            backups = self.file_handler.list_backups()
            if not backups:
                print("No backups found.")
            else:
                print(f"\nFound {len(backups)} backup file(s):")
                print("-" * 65)
                print(f"{'Filename':<40} {'Size':>10} {'Created At':<20}")
                print("-" * 65)
                for b in backups:
                    size_str = f"{b['size_bytes']} B"
                    print(f"{b['filename']:<40} {size_str:>10} {b['created_at']:<20}")
                print("-" * 65)
        elif opt == "3":
            backups = self.file_handler.list_backups()
            if not backups:
                print("No backups available to restore.")
                return

            print("\nAvailable backups for restore:")
            for idx, b in enumerate(backups, start=1):
                print(f"  {idx}. {b['filename']} ({b['created_at']})")

            sel = input(f"\nEnter number to restore (1-{len(backups)}) or press Enter to cancel: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(backups):
                target_backup = backups[int(sel) - 1]["filename"]
                confirm = input(f"Are you sure you want to restore '{target_backup}'? Current state will be overwritten. (y/N): ").strip().lower()
                if confirm in ("y", "yes"):
                    success = self.file_handler.restore_backup(target_backup)
                    if success:
                        self.load_data()
                        print("Backup restored successfully and data reloaded!")
                    else:
                        print("Failed to restore backup.")
            else:
                print("Restore cancelled.")
        elif opt == "0":
            return
        else:
            print("Invalid option.")

def main():
    tracker = FinanceTracker()
    tracker.run()

if __name__ == "__main__":
    main()
