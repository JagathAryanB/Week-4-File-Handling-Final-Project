import os
from datetime import datetime

DIARY_FILE = "my_diary.txt"

def add_entry():
    print("\n--- NEW DIARY ENTRY ---")
    title = input("Entry title: ").strip()
    print("Write your thoughts (press Enter, then type END on a new line to finish):")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break

    content = "\n".join(lines)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry_block = (
        f"\n{'='*50}\n"
        f"DATE  : {timestamp}\n"
        f"TITLE : {title}\n"
        f"{'-'*50}\n"
        f"{content}\n"
        f"{'='*50}\n"
    )

    try:
        with open(DIARY_FILE, "a", encoding="utf-8") as file:
            file.write(entry_block)
        print("[Success] Diary entry saved successfully!")
    except OSError as e:
        print(f"[Error] Could not save entry: {e}")

def view_entries():
    print("\n--- VIEW DIARY ENTRIES ---")
    if not os.path.exists(DIARY_FILE):
        print("Your diary is empty. No entries written yet.")
        return

    try:
        with open(DIARY_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            if content.strip():
                print(content)
            else:
                print("Diary file is empty.")
    except OSError as e:
        print(f"[Error] Failed to read diary: {e}")

def search_entries():
    print("\n--- SEARCH DIARY ---")
    if not os.path.exists(DIARY_FILE):
        print("Diary is empty. No entries to search.")
        return

    keyword = input("Enter search keyword: ").strip().lower()
    if not keyword:
        print("Search cancelled.")
        return

    try:
        with open(DIARY_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            entries = content.split("=" * 50)
            matched = [e for e in entries if keyword in e.lower() and e.strip()]

        print(f"\nFound {len(matched)} matching entry/entries:")
        for idx, entry in enumerate(matched, start=1):
            print(f"\n[Result #{idx}]")
            print(f"{'='*50}{entry}{'='*50}")
    except OSError as e:
        print(f"[Error] Search failed: {e}")

def main():
    while True:
        print("\n=== PERSONAL DIARY & NOTES APP ===")
        print("1. Write New Entry")
        print("2. Read All Entries")
        print("3. Search Entries")
        print("0. Exit")
        choice = input("Select an option (0-3): ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            search_entries()
        elif choice == "0":
            print("Goodbye! Take care.")
            break
        else:
            print("Invalid option. Please choose 0-3.")

if __name__ == "__main__":
    main()
