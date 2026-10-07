import unittest
import tempfile
import shutil
import os
import json
from finance_tracker.file_handler import FileHandler
from finance_tracker.expense import Expense

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.handler = FileHandler(base_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_json_save_and_load(self):
        sample_data = {
            "expenses": [
                {
                    "id": "abc1",
                    "date": "2026-10-01",
                    "amount": 25.50,
                    "category": "Food & Dining",
                    "description": "Pizza dinner",
                    "is_recurring": False,
                    "created_at": "2026-10-01T20:00:00"
                }
            ],
            "budgets": {"2026-10": {"overall": 300.0, "categories": {}}}
        }

        save_success = self.handler.save_to_json(sample_data)
        self.assertTrue(save_success)
        self.assertTrue(os.path.exists(self.handler.data_file))

        loaded_data = self.handler.load_from_json()
        self.assertEqual(len(loaded_data["expenses"]), 1)
        self.assertEqual(loaded_data["expenses"][0]["id"], "abc1")
        self.assertEqual(loaded_data["budgets"]["2026-10"]["overall"], 300.0)

    def test_load_nonexistent_file(self):
        non_existent_path = os.path.join(self.test_dir, "missing.json")
        data = self.handler.load_from_json(non_existent_path)
        self.assertIn("expenses", data)
        self.assertIn("budgets", data)
        self.assertEqual(len(data["expenses"]), 0)

    def test_load_corrupted_json(self):
        corrupt_file = os.path.join(self.test_dir, "corrupt.json")
        with open(corrupt_file, "w", encoding="utf-8") as f:
            f.write("{ this is completely invalid json :! }")

        data = self.handler.load_from_json(corrupt_file)
        self.assertEqual(data, {"expenses": [], "budgets": {}})

    def test_backup_and_restore(self):
        data = {"expenses": [{"id": "b1", "date": "2026-10-01", "amount": 10.0, "category": "Food", "description": "Tea", "is_recurring": False}], "budgets": {}}
        self.handler.save_to_json(data)

        backup_path = self.handler.create_backup("test_backup")
        self.assertIsNotNone(backup_path)
        self.assertTrue(os.path.exists(backup_path))

        backups = self.handler.list_backups()
        self.assertTrue(len(backups) >= 1)

        mutated_data = {"expenses": [], "budgets": {}}
        self.handler.save_to_json(mutated_data)
        self.assertEqual(len(self.handler.load_from_json()["expenses"]), 0)

        restore_success = self.handler.restore_backup(os.path.basename(backup_path))
        self.assertTrue(restore_success)

        restored_data = self.handler.load_from_json()
        self.assertEqual(len(restored_data["expenses"]), 1)
        self.assertEqual(restored_data["expenses"][0]["id"], "b1")

    def test_csv_export_and_import(self):
        expenses = [
            Expense("2026-10-01", 12.50, "Food & Dining", "Sandwich", expense_id="c1"),
            Expense("2026-10-02", 5.00, "Transportation", "Train", expense_id="c2", is_recurring=True)
        ]

        csv_path = self.handler.export_to_csv(expenses, custom_filename="test_export.csv")
        self.assertIsNotNone(csv_path)
        self.assertTrue(os.path.exists(csv_path))

        imported_exps, errors = self.handler.import_from_csv(csv_path)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(imported_exps), 2)
        self.assertEqual(imported_exps[0].id, "c1")
        self.assertEqual(imported_exps[0].amount, 12.50)
        self.assertTrue(imported_exps[1].is_recurring)

    def test_csv_import_with_invalid_rows(self):
        bad_csv_path = os.path.join(self.test_dir, "bad.csv")
        with open(bad_csv_path, "w", encoding="utf-8") as f:
            f.write("id,date,category,amount,description,is_recurring\n")
            f.write("1,2026-10-01,Food,20.0,Valid Row,false\n")
            f.write("2,invalid-date,Food,30.0,Bad Date,false\n")
            f.write("3,2026-10-02,Food,-5.0,Bad Negative Amount,false\n")

        imported_exps, errors = self.handler.import_from_csv(bad_csv_path)
        self.assertEqual(len(imported_exps), 1)
        self.assertEqual(len(errors), 2)

if __name__ == "__main__":
    unittest.main()
