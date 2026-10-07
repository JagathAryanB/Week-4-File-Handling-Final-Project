from typing import List, Optional, Dict, Any
from datetime import datetime
from .expense import Expense
from .utils import validate_date_str

class ExpenseManager:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.budgets: Dict[str, Dict[str, Any]] = {}

    def add_expense(self, expense: Expense) -> Expense:
        if not isinstance(expense, Expense):
            raise TypeError("Expected an instance of Expense.")
        self.expenses.append(expense)
        return expense

    def remove_expense(self, expense_id: str) -> bool:
        expense_id = expense_id.strip()
        for idx, exp in enumerate(self.expenses):
            if exp.id == expense_id:
                del self.expenses[idx]
                return True
        return False

    def get_expense_by_id(self, expense_id: str) -> Optional[Expense]:
        expense_id = expense_id.strip()
        for exp in self.expenses:
            if exp.id == expense_id:
                return exp
        return None

    def get_all_expenses(self, sort_by: str = "date", reverse: bool = True) -> List[Expense]:
        if sort_by == "amount":
            return sorted(self.expenses, key=lambda x: x.amount, reverse=reverse)
        elif sort_by == "category":
            return sorted(self.expenses, key=lambda x: x.category.lower(), reverse=reverse)
        else:
            return sorted(self.expenses, key=lambda x: x.date, reverse=reverse)

    def search_expenses(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None
    ) -> List[Expense]:
        results = self.expenses

        if keyword:
            kw = keyword.lower().strip()
            results = [
                e for e in results
                if kw in e.description.lower() or kw in e.category.lower() or kw in e.id.lower()
            ]

        if category:
            cat = category.lower().strip()
            results = [e for e in results if e.category.lower() == cat]

        if start_date and validate_date_str(start_date):
            results = [e for e in results if e.date >= start_date.strip()]

        if end_date and validate_date_str(end_date):
            results = [e for e in results if e.date <= end_date.strip()]

        if min_amount is not None:
            results = [e for e in results if e.amount >= min_amount]

        if max_amount is not None:
            results = [e for e in results if e.amount <= max_amount]

        return sorted(results, key=lambda x: x.date, reverse=True)

    def get_expenses_by_month(self, year: int, month: int) -> List[Expense]:
        month_prefix = f"{year:04d}-{month:02d}"
        return [e for e in self.expenses if e.date.startswith(month_prefix)]

    def get_total_expenses(self, expenses: Optional[List[Expense]] = None) -> float:
        target = self.expenses if expenses is None else expenses
        return round(sum(e.amount for e in target), 2)

    def get_recurring_expenses(self) -> List[Expense]:
        return [e for e in self.expenses if e.is_recurring]

    def set_budget(self, month_key: str, amount: float, category: Optional[str] = None) -> None:
        if month_key not in self.budgets:
            self.budgets[month_key] = {"overall": 0.0, "categories": {}}

        if category:
            self.budgets[month_key]["categories"][category] = round(amount, 2)
        else:
            self.budgets[month_key]["overall"] = round(amount, 2)

    def get_budget(self, month_key: str, category: Optional[str] = None) -> Optional[float]:
        if month_key not in self.budgets:
            return None
        month_cfg = self.budgets[month_key]
        if category:
            return month_cfg.get("categories", {}).get(category)
        return month_cfg.get("overall")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "expenses": [e.to_dict() for e in self.expenses],
            "budgets": self.budgets
        }

    def load_from_dict(self, data: Dict[str, Any]) -> None:
        self.expenses.clear()
        self.budgets.clear()

        raw_expenses = data.get("expenses", [])
        for item in raw_expenses:
            try:
                exp = Expense.from_dict(item)
                self.expenses.append(exp)
            except Exception:
                pass

        self.budgets = data.get("budgets", {})
