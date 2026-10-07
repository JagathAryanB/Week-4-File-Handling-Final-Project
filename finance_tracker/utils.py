from datetime import datetime
import os
import sys

DATE_FORMAT = "%Y-%m-%d"

def get_today_str() -> str:
    return datetime.now().strftime(DATE_FORMAT)

def validate_date_str(date_str: str) -> bool:
    if not isinstance(date_str, str):
        return False
    try:
        parsed = datetime.strptime(date_str.strip(), DATE_FORMAT)
        if parsed.year < 1900 or parsed.year > 2100:
            return False
        return True
    except ValueError:
        return False

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str.strip(), DATE_FORMAT)

def format_currency(amount: float) -> str:
    try:
        return f"${amount:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def render_ascii_bar(percentage: float, width: int = 20) -> str:
    clamped_pct = max(0.0, min(100.0, percentage))
    filled_blocks = int(round((clamped_pct / 100.0) * width))
    empty_blocks = max(0, width - filled_blocks)
    
    bar = "#" * filled_blocks + "-" * empty_blocks
    return f"[{bar}] {percentage:5.1f}%"

def print_box(title: str, width: int = 60) -> None:
    print("=" * width)
    print(title.center(width))
    print("=" * width)

def prompt_non_empty(prompt_text: str, default: str = None) -> str:
    prompt_msg = f"{prompt_text} [{default}]: " if default else f"{prompt_text}: "
    while True:
        try:
            val = input(prompt_msg).strip()
            if not val and default is not None:
                return default
            if val:
                return val
            print("Error: Input cannot be empty. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            raise

def prompt_float(prompt_text: str, min_val: float = 0.01, max_val: float = 1_000_000_000.0) -> float:
    while True:
        try:
            val_str = input(f"{prompt_text}: ").strip()
            cleaned = val_str.replace("$", "").replace(",", "")
            amount = float(cleaned)
            if amount < min_val:
                print(f"Error: Amount must be at least {format_currency(min_val)}.")
                continue
            if amount > max_val:
                print(f"Error: Amount exceeds maximum permitted limit ({format_currency(max_val)}).")
                continue
            return round(amount, 2)
        except ValueError:
            print("Error: Invalid numeric amount. Please enter a valid number (e.g. 45.50).")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            raise

def prompt_date(prompt_text: str, default_today: bool = True) -> str:
    today = get_today_str()
    prompt_msg = f"{prompt_text} (YYYY-MM-DD) [Default: {today}]: " if default_today else f"{prompt_text} (YYYY-MM-DD): "
    while True:
        try:
            val = input(prompt_msg).strip()
            if not val and default_today:
                return today
            if validate_date_str(val):
                return val
            print("Error: Invalid date format. Please use YYYY-MM-DD (e.g. 2026-10-07).")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            raise

def prompt_choice(prompt_text: str, valid_choices: list[str]) -> str:
    valid_lower = [str(c).strip().lower() for c in valid_choices]
    while True:
        try:
            val = input(f"{prompt_text}: ").strip()
            if val.lower() in valid_lower:
                idx = valid_lower.index(val.lower())
                return valid_choices[idx]
            print(f"Error: Invalid choice. Available options: {', '.join(valid_choices)}")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            raise
