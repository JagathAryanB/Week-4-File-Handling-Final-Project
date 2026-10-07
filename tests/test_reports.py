import unittest
from finance_tracker.expense import Expense
from finance_tracker.reports import ReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.expenses = [
            Expense("2026-10-01", 100.0, "Food & Dining", "Groceries"),
            Expense("2026-10-02", 50.0, "Transportation", "Fuel"),
            Expense("2026-10-05", 150.0, "Food & Dining", "Dinner party"),
            Expense("2026-09-15", 80.0, "Utilities", "Old Electric bill")
        ]

    def test_monthly_summary(self):
        summary = ReportGenerator.generate_monthly_summary(
            self.expenses,
            year=2026,
            month=10,
            budget=500.0
        )
        self.assertEqual(summary["total_spent"], 300.0)
        self.assertEqual(summary["transaction_count"], 3)
        self.assertEqual(summary["highest_expense"].amount, 150.0)
        self.assertEqual(summary["lowest_expense"].amount, 50.0)

        self.assertIsNotNone(summary["budget_info"])
        self.assertEqual(summary["budget_info"]["remaining"], 200.0)
        self.assertEqual(summary["budget_info"]["percentage_used"], 60.0)
        self.assertFalse(summary["budget_info"]["is_over"])

    def test_category_breakdown(self):
        oct_exps = [e for e in self.expenses if e.date.startswith("2026-10")]
        breakdown = ReportGenerator.generate_category_breakdown(oct_exps)

        self.assertEqual(len(breakdown), 2)
        self.assertEqual(breakdown[0]["category"], "Food & Dining")
        self.assertEqual(breakdown[0]["amount"], 250.0)
        self.assertEqual(breakdown[0]["count"], 2)
        self.assertAlmostEqual(breakdown[0]["percentage"], 83.3, places=1)
        self.assertIn("#", breakdown[0]["bar"])

    def test_trend_analysis(self):
        trends = ReportGenerator.generate_trend_analysis(self.expenses, max_months=3)
        self.assertEqual(len(trends), 2)
        self.assertEqual(trends[0]["month_key"], "2026-09")
        self.assertEqual(trends[0]["amount"], 80.0)
        self.assertEqual(trends[1]["month_key"], "2026-10")
        self.assertEqual(trends[1]["amount"], 300.0)
        self.assertGreater(trends[1]["change_percentage"], 0)

    def test_predict_month_end(self):
        prediction = ReportGenerator.predict_month_end(self.expenses, 2026, 10)
        self.assertEqual(prediction["total_so_far"], 300.0)
        self.assertTrue(prediction["projected_total"] > 0)
        self.assertEqual(prediction["total_days"], 31)

    def test_format_monthly_report_text(self):
        summary = ReportGenerator.generate_monthly_summary(
            self.expenses,
            year=2026,
            month=10,
            budget=500.0
        )
        report_text = ReportGenerator.format_monthly_report_text(summary)
        self.assertIn("MONTHLY EXPENSE REPORT: October 2026", report_text)
        self.assertIn("$300.00", report_text)
        self.assertIn("BUDGET TRACKING:", report_text)
        self.assertIn("CATEGORY BREAKDOWN:", report_text)

if __name__ == "__main__":
    unittest.main()
