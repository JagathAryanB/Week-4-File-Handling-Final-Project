import json
import os
from datetime import datetime

TODO_FILE = "todo_storage.json"

class TodoList:
    def __init__(self, filepath=TODO_FILE):
        self.filepath = filepath
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] Could not load tasks ({e}), starting empty.")
            return []

    def save_tasks(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=4)
            return True
        except OSError as e:
            print(f"[Error] Failed to save tasks: {e}")
            return False

    def add_task(self, title):
        task = {
            "id": len(self.tasks) + 1,
            "title": title.strip(),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"[Success] Added task #{task['id']}: '{task['title']}'")

    def list_tasks(self):
        print("\n=== CURRENT TO-DO LIST ===")
        if not self.tasks:
            print("Your to-do list is empty! All caught up.")
            return

        print(f"{'#':<4} {'Status':<10} {'Task Title':<35} {'Created':<16}")
        print("-" * 68)
        for t in self.tasks:
            status = "[x] DONE" if t["completed"] else "[ ] PENDING"
            print(f"{t['id']:<4} {status:<10} {t['title']:<35} {t['created_at']:<16}")
        print("-" * 68)

    def complete_task(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = True
                self.save_tasks()
                print(f"[Success] Task #{task_id} marked as completed!")
                return
        print(f"[Error] Task #{task_id} not found.")

    def delete_task(self, task_id):
        for idx, t in enumerate(self.tasks):
            if t["id"] == task_id:
                deleted = self.tasks.pop(idx)
                for i, rem in enumerate(self.tasks, start=1):
                    rem["id"] = i
                self.save_tasks()
                print(f"[Success] Deleted task: '{deleted['title']}'")
                return
        print(f"[Error] Task #{task_id} not found.")

def main():
    todo = TodoList()
    while True:
        print("\n--- PERSISTENT TO-DO MANAGER ---")
        print("1. View Tasks")
        print("2. Add New Task")
        print("3. Mark Task Completed")
        print("4. Delete Task")
        print("0. Exit")

        choice = input("Select an option (0-4): ").strip()
        if choice == "1":
            todo.list_tasks()
        elif choice == "2":
            title = input("Enter task description: ").strip()
            if title:
                todo.add_task(title)
        elif choice == "3":
            tid = input("Enter task # to mark complete: ").strip()
            if tid.isdigit():
                todo.complete_task(int(tid))
        elif choice == "4":
            tid = input("Enter task # to delete: ").strip()
            if tid.isdigit():
                todo.delete_task(int(tid))
        elif choice == "0":
            print("Exiting To-Do Manager. State is safely persisted!")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
