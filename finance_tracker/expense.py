from datetime import datetime
import uuid
from typing import Dict, Any
from .utils import validate_date_str, format_currency

DEFAULT_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Housing & Rent",
    "Utilities & Bills",
    "Entertainment & Leisure",
    "Healthcare & Medical",
    "Education & Books",
    "Shopping & Groceries",
    "Personal & Wellness",
    "Miscellaneous"
]

class Expense:
    def __init__(
        self,
        date: str,
        amount: float,
        category: str,
        description: str,
        expense_id: str = None,
        is_recurring: bool = False,
        created_at: str = None
    ):
        self.date = self.validate_date(date)
        self.amount = self.validate_amount(amount)
        self.category = self.validate_category(category)
        self.description = self.validate_description(description)
        self.is_recurring = bool(is_recurring)
        self.id = expense_id if expense_id else str(uuid.uuid4())[:8]
        self.created_at = created_at if created_at else datetime.now().isoformat()

    @staticmethod
    def validate_date(date_str: str) -> str:
        if not validate_date_str(date_str):
            raise ValueError(f"Invalid date '{date_str}'. Expected format is YYYY-MM-DD.")
        return date_str.strip()

    @staticmethod
    def validate_amount(amount: Any) -> float:
        try:
            val = float(amount)
        except (ValueError, TypeError):
            raise ValueError(f"Amount must be a numeric value, got '{amount}'.")

        if val <= 0:
            raise ValueError(f"Amount must be greater than zero, got {val}.")
        return round(val, 2)

    @staticmethod
    def validate_category(category: str) -> str:
        if not category or not isinstance(category, str) or not category.strip():
            raise ValueError("Category cannot be empty.")
        return category.strip()

    @staticmethod
    def validate_description(description: str) -> str:
        if not description or not isinstance(description, str) or not description.strip():
            raise ValueError("Description cannot be empty.")
        return description.strip()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "is_recurring": self.is_recurring,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        required_keys = ("date", "amount", "category", "description")
        for key in required_keys:
            if key not in data:
                raise KeyError(f"Missing required field '{key}' in expense data.")

        return cls(
            date=str(data["date"]),
            amount=data["amount"],
            category=str(data["category"]),
            description=str(data["description"]),
            expense_id=str(data.get("id", "")) or None,
            is_recurring=bool(data.get("is_recurring", False)),
            created_at=data.get("created_at")
        )

    def __repr__(self) -> str:
        recurring_mark = " (Recurring)" if self.is_recurring else ""
        return (
            f"Expense(id='{self.id}', date='{self.date}', "
            f"amount={format_currency(self.amount)}, category='{self.category}', "
            f"description='{self.description}'{recurring_mark})"
        )

    def __str__(self) -> str:
        recurring_mark = " [Recurring]" if self.is_recurring else ""
        return f"{self.date} | {self.category:<18} | {format_currency(self.amount):>10} | {self.description}{recurring_mark}"
