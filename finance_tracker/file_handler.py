import os
import json
import csv
import shutil
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from .expense import Expense

DEFAULT_BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data")
)

class FileHandler:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = os.path.abspath(base_dir) if base_dir else DEFAULT_BASE_DIR
        self.data_file = os.path.join(self.base_dir, "expenses.json")
        self.backup_dir = os.path.join(self.base_dir, "backup")
        self.exports_dir = os.path.join(self.base_dir, "exports")

        self.ensure_directories()

    def ensure_directories(self) -> None:
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            os.makedirs(self.backup_dir, exist_ok=True)
            os.makedirs(self.exports_dir, exist_ok=True)
        except OSError as e:
            print(f"Warning: Failed to create directories at '{self.base_dir}': {e}")

    def save_to_json(self, data: Dict[str, Any], target_path: Optional[str] = None) -> bool:
        filepath = target_path or self.data_file
        try:
            temp_path = f"{filepath}.tmp"
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            
            if os.path.exists(filepath):
                os.replace(temp_path, filepath)
            else:
                os.rename(temp_path, filepath)
            return True
        except PermissionError as e:
            print(f"Error: Permission denied when saving data to '{filepath}': {e}")
            return False
        except OSError as e:
            print(f"Error: Failed to write data to '{filepath}': {e}")
            return False

    def load_from_json(self, source_path: Optional[str] = None) -> Dict[str, Any]:
        filepath = source_path or self.data_file

        if not os.path.exists(filepath):
            default_data = {"expenses": [], "budgets": {}}
            self.save_to_json(default_data, filepath)
            return default_data

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError("JSON root must be an object/dict.")
                return data
        except json.JSONDecodeError as e:
            print(f"\n[Warning] File '{filepath}' is corrupted: {e}")
            corrupt_backup = f"{filepath}.corrupted.{int(datetime.now().timestamp())}"
            try:
                shutil.copy2(filepath, corrupt_backup)
                print(f"A quarantine copy of corrupted file saved to '{corrupt_backup}'.")
            except Exception:
                pass
            return {"expenses": [], "budgets": {}}
        except PermissionError as e:
            print(f"Error: Permission denied reading '{filepath}': {e}")
            return {"expenses": [], "budgets": {}}
        except Exception as e:
            print(f"Unexpected error while reading '{filepath}': {e}")
            return {"expenses": [], "budgets": {}}

    def create_backup(self, custom_label: Optional[str] = None) -> Optional[str]:
        if not os.path.exists(self.data_file):
            print("Error: No data file found to back up.")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        label_part = f"_{custom_label.strip()}" if custom_label else ""
        backup_filename = f"expenses_backup_{timestamp}{label_part}.json"
        dest_path = os.path.join(self.backup_dir, backup_filename)

        try:
            shutil.copy2(self.data_file, dest_path)
            return dest_path
        except (PermissionError, OSError) as e:
            print(f"Error: Failed to create backup: {e}")
            return None

    def list_backups(self) -> List[Dict[str, Any]]:
        if not os.path.isdir(self.backup_dir):
            return []

        backups = []
        try:
            for entry in os.scandir(self.backup_dir):
                if entry.is_file() and entry.name.endswith(".json"):
                    stat = entry.stat()
                    backups.append({
                        "filename": entry.name,
                        "path": entry.path,
                        "size_bytes": stat.st_size,
                        "created_at": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
        except OSError as e:
            print(f"Error listing backups: {e}")

        return sorted(backups, key=lambda x: x["filename"], reverse=True)

    def restore_backup(self, backup_filename: str) -> bool:
        backup_path = os.path.join(self.backup_dir, backup_filename)
        if not os.path.isfile(backup_path):
            print(f"Error: Backup file '{backup_filename}' does not exist.")
            return False

        if os.path.exists(self.data_file):
            self.create_backup("pre_restore_safety")

        try:
            with open(backup_path, "r", encoding="utf-8") as f:
                json.load(f)
            
            shutil.copy2(backup_path, self.data_file)
            return True
        except json.JSONDecodeError:
            print("Error: Selected backup file contains corrupted JSON and cannot be restored.")
            return False
        except (PermissionError, OSError) as e:
            print(f"Error restoring backup: {e}")
            return False

    def export_to_csv(self, expenses: List[Expense], custom_filename: Optional[str] = None) -> Optional[str]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = custom_filename or f"expenses_export_{timestamp}.csv"
        if not filename.endswith(".csv"):
            filename += ".csv"

        filepath = os.path.join(self.exports_dir, filename)

        fieldnames = ["id", "date", "category", "amount", "description", "is_recurring", "created_at"]
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for exp in expenses:
                    writer.writerow(exp.to_dict())
            return filepath
        except (PermissionError, OSError) as e:
            print(f"Error exporting CSV: {e}")
            return None

    def import_from_csv(self, filepath: str) -> Tuple[List[Expense], List[str]]:
        if not os.path.isfile(filepath):
            return [], [f"File not found: '{filepath}'"]

        imported_expenses: List[Expense] = []
        errors: List[str] = []

        try:
            with open(filepath, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                if not reader.fieldnames:
                    return [], ["CSV file is empty or headers are missing."]

                required_cols = {"date", "category", "amount", "description"}
                headers = {h.strip().lower() for h in reader.fieldnames}
                missing_cols = required_cols - headers
                if missing_cols:
                    return [], [f"Missing required columns in CSV: {', '.join(missing_cols)}"]

                for line_num, row in enumerate(reader, start=2):
                    cleaned_row = {k.strip().lower(): v for k, v in row.items() if k}
                    try:
                        exp = Expense(
                            date=cleaned_row.get("date", ""),
                            amount=cleaned_row.get("amount", 0),
                            category=cleaned_row.get("category", ""),
                            description=cleaned_row.get("description", ""),
                            expense_id=cleaned_row.get("id"),
                            is_recurring=str(cleaned_row.get("is_recurring", "")).lower() in ("true", "1", "yes")
                        )
                        imported_expenses.append(exp)
                    except Exception as err:
                        errors.append(f"Row {line_num}: {err}")
        except Exception as e:
            errors.append(f"Could not read CSV file: {e}")

        return imported_expenses, errors

    def export_text_report(self, report_content: str, filename_prefix: str = "report") -> Optional[str]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.txt"
        filepath = os.path.join(self.exports_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(report_content)
            return filepath
        except (PermissionError, OSError) as e:
            print(f"Error saving report text: {e}")
            return None
