import os
from datetime import datetime

DATA_FILE = "user_data.txt"

def save_user_profile():
    print("=== SAVE USER DATA TO TEXT FILE ===")
    name = input("Enter your full name: ").strip()
    email = input("Enter your email address: ").strip()
    age = input("Enter your age: ").strip()
    occupation = input("Enter your occupation: ").strip()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = (
        f"----------------------------------------\n"
        f"Saved At   : {timestamp}\n"
        f"Name       : {name}\n"
        f"Email      : {email}\n"
        f"Age        : {age}\n"
        f"Occupation : {occupation}\n"
        f"----------------------------------------\n"
    )

    try:
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"\n[Success] User data appended to '{DATA_FILE}' successfully!")
    except OSError as e:
        print(f"[Error] Failed to write to file: {e}")

def view_saved_data():
    if not os.path.exists(DATA_FILE):
        print(f"\n[Info] No saved data found. File '{DATA_FILE}' does not exist yet.")
        return

    print("\n=== SAVED USER DATA RECORDS ===")
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                print(content)
            else:
                print("File is currently empty.")
    except OSError as e:
        print(f"[Error] Failed to read file: {e}")

if __name__ == "__main__":
    save_user_profile()
    view_saved_data()
