import unittest
from finance_tracker.expense import Expense, DEFAULT_CATEGORIES
from finance_tracker.expense_manager import ExpenseManager

class TestExpenseModel(unittest.TestCase):
    def test_valid_expense_creation(self):
        exp = Expense(
            date="2026-10-07",
            amount=45.50,
            category="Food & Dining",
            description="Lunch meal",
            is_recurring=False
        )
        self.assertEqual(exp.date, "2026-10-07")
        self.assertEqual(exp.amount, 45.50)
        self.assertEqual(exp.category, "Food & Dining")
        self.assertEqual(exp.description, "Lunch meal")
        self.assertFalse(exp.is_recurring)
        self.assertTrue(len(exp.id) > 0)

    def test_invalid_date_formats(self):
        invalid_dates = ["2026/10/07", "07-10-2026", "invalid-date", "2026-02-30", ""]
        for d in invalid_dates:
            with self.subTest(date=d):
                with self.assertRaises(ValueError):
                    Expense(date=d, amount=10.0, category="Food", description="Test")

    def test_invalid_amounts(self):
        invalid_amounts = [0, -5.0, -100, "abc", None]
        for a in invalid_amounts:
            with self.subTest(amount=a):
                with self.assertRaises(ValueError):
                    Expense(date="2026-10-07", amount=a, category="Food", description="Test")

    def test_invalid_category_and_description(self):
        with self.assertRaises(ValueError):
            Expense(date="2026-10-07", amount=10.0, category="", description="Test")

        with self.assertRaises(ValueError):
            Expense(date="2026-10-07", amount=10.0, category="Food", description="   ")

    def test_dict_serialization(self):
        exp = Expense(
            date="2026-10-07",
            amount=99.99,
            category="Utilities",
            description="Electricity Bill",
            expense_id="exp-001",
            is_recurring=True
        )
        d = exp.to_dict()
        self.assertEqual(d["id"], "exp-001")
        self.assertEqual(d["amount"], 99.99)
        self.assertTrue(d["is_recurring"])

        reconstructed = Expense.from_dict(d)
        self.assertEqual(reconstructed.id, exp.id)
        self.assertEqual(reconstructed.amount, exp.amount)
        self.assertEqual(reconstructed.category, exp.category)
        self.assertEqual(reconstructed.is_recurring, exp.is_recurring)

class TestExpenseManager(unittest.TestCase):
    def setUp(self):
        self.manager = ExpenseManager()
        self.e1 = Expense("2026-10-01", 50.0, "Food & Dining", "Grocery", expense_id="1")
        self.e2 = Expense("2026-10-02", 20.0, "Transportation", "Bus ticket", expense_id="2")
        self.e3 = Expense("2026-10-05", 150.0, "Utilities", "Internet bill", expense_id="3")
        self.manager.add_expense(self.e1)
        self.manager.add_expense(self.e2)
        self.manager.add_expense(self.e3)

    def test_add_and_remove_expense(self):
        self.assertEqual(len(self.manager.expenses), 3)
        removed = self.manager.remove_expense("2")
        self.assertTrue(removed)
        self.assertEqual(len(self.manager.expenses), 2)
        self.assertIsNone(self.manager.get_expense_by_id("2"))

    def test_get_total_expenses(self):
        self.assertEqual(self.manager.get_total_expenses(), 220.0)

    def test_search_by_keyword(self):
        results = self.manager.search_expenses(keyword="internet")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "3")

    def test_search_by_category(self):
        results = self.manager.search_expenses(category="transportation")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "2")

    def test_search_by_date_range(self):
        results = self.manager.search_expenses(start_date="2026-10-02", end_date="2026-10-05")
        self.assertEqual(len(results), 2)

    def test_search_by_amount_range(self):
        results = self.manager.search_expenses(min_amount=30.0, max_amount=100.0)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "1")

    def test_budget_management(self):
        self.manager.set_budget("2026-10", 500.0)
        self.assertEqual(self.manager.get_budget("2026-10"), 500.0)
        self.assertIsNone(self.manager.get_budget("2026-11"))

if __name__ == "__main__":
    unittest.main()
