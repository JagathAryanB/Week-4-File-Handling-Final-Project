import json
import os
from datetime import datetime

SCORES_FILE = "quiz_scores.json"

QUESTIONS = [
    {
        "q": "Which mode is used in Python open() to append data without overwriting?",
        "options": ["A. 'w'", "B. 'a'", "C. 'r'", "D. 'x'"],
        "answer": "B"
    },
    {
        "q": "What Python statement guarantees files are safely closed after execution?",
        "options": ["A. try/catch", "B. using", "C. with", "D. close"],
        "answer": "C"
    },
    {
        "q": "Which module in Python is used for reading comma-separated files?",
        "options": ["A. csv", "B. json", "C. sys", "D. os"],
        "answer": "A"
    },
    {
        "q": "Which exception is raised when trying to open a non-existent file for reading?",
        "options": ["A. ValueError", "B. FileNotFoundError", "C. KeyError", "D. PermissionError"],
        "answer": "B"
    },
    {
        "q": "In json module, which method deserializes a JSON string into a Python dict?",
        "options": ["A. json.dump()", "B. json.write()", "C. json.loads()", "D. json.encode()"],
        "answer": "C"
    }
]

def load_leaderboard():
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_score(player_name, score, total):
    leaderboard = load_leaderboard()
    percentage = round((score / total) * 100, 1)
    entry = {
        "player": player_name,
        "score": score,
        "total": total,
        "percentage": percentage,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    leaderboard.append(entry)
    leaderboard.sort(key=lambda x: x["percentage"], reverse=True)

    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=4)

def show_leaderboard():
    leaderboard = load_leaderboard()
    print("\n" + "=" * 50)
    print("           QUIZ LEADERBOARD")
    print("=" * 50)
    if not leaderboard:
        print("No quiz scores recorded yet.")
        return

    print(f"{'Rank':<6} {'Player':<18} {'Score':<10} {'Date':<15}")
    print("-" * 50)
    for rank, entry in enumerate(leaderboard[:10], start=1):
        score_str = f"{entry['score']}/{entry['total']} ({entry['percentage']}%)"
        print(f"{rank:<6} {entry['player']:<18} {score_str:<10} {entry['date']:<15}")
    print("=" * 50)

def play_quiz():
    print("=" * 50)
    print("      PYTHON FILE HANDLING QUIZ GAME")
    print("=" * 50)
    player = input("Enter your name: ").strip() or "Anonymous"

    score = 0
    for idx, item in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {idx}/{len(QUESTIONS)}:")
        print(item["q"])
        for opt in item["options"]:
            print(f"  {opt}")

        ans = input("Your answer (A/B/C/D): ").strip().upper()
        if ans == item["answer"]:
            print("[Correct! +1 point]")
            score += 1
        else:
            print(f"[Incorrect! Correct answer was: {item['answer']}]")

    print("\n" + "=" * 50)
    print(f"Quiz Complete! Final Score for {player}: {score}/{len(QUESTIONS)}")
    save_score(player, score, len(QUESTIONS))
    print(f"Score persisted to '{SCORES_FILE}' successfully.")
    show_leaderboard()

if __name__ == "__main__":
    play_quiz()
