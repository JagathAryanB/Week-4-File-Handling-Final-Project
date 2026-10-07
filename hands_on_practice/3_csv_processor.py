import csv
import os

SAMPLE_CSV = "students_data.csv"
SUMMARY_CSV = "students_summary.csv"

def generate_sample_csv():
    data = [
        {"Student_ID": "S101", "Name": "Alice Johnson", "Subject": "Python", "Score": 92},
        {"Student_ID": "S102", "Name": "Bob Smith", "Subject": "Python", "Score": 78},
        {"Student_ID": "S103", "Name": "Charlie Brown", "Subject": "Python", "Score": 85},
        {"Student_ID": "S104", "Name": "Diana Prince", "Subject": "Python", "Score": 96},
        {"Student_ID": "S105", "Name": "Evan Wright", "Subject": "Python", "Score": 64},
    ]
    with open(SAMPLE_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Student_ID", "Name", "Subject", "Score"])
        writer.writeheader()
        writer.writerows(data)
    print(f"[Created] Sample CSV generated at '{SAMPLE_CSV}'.")

def process_csv_data():
    if not os.path.exists(SAMPLE_CSV):
        generate_sample_csv()

    records = []
    try:
        with open(SAMPLE_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    records.append({
                        "id": row["Student_ID"],
                        "name": row["Name"],
                        "subject": row["Subject"],
                        "score": float(row["Score"])
                    })
                except (ValueError, KeyError) as err:
                    print(f"Skipping malformed row: {err}")
    except OSError as e:
        print(f"[Error] Failed to open CSV file: {e}")
        return

    if not records:
        print("No valid student records found in CSV.")
        return

    scores = [r["score"] for r in records]
    avg_score = sum(scores) / len(scores)
    max_record = max(records, key=lambda x: x["score"])
    min_record = min(records, key=lambda x: x["score"])

    print("\n=== STUDENT CSV DATA REPORT ===")
    print(f"{'ID':<8} {'Name':<20} {'Subject':<10} {'Score':>6}")
    print("-" * 50)
    for r in records:
        print(f"{r['id']:<8} {r['name']:<20} {r['subject']:<10} {r['score']:>6.1f}")
    print("-" * 50)
    print(f"Total Students : {len(records)}")
    print(f"Average Score  : {avg_score:.2f}")
    print(f"Highest Score  : {max_record['score']} ({max_record['name']})")
    print(f"Lowest Score   : {min_record['score']} ({min_record['name']})")

    summary_data = [
        {"Metric": "Total Students", "Value": str(len(records))},
        {"Metric": "Average Score", "Value": f"{avg_score:.2f}"},
        {"Metric": "Highest Scorer", "Value": f"{max_record['name']} ({max_record['score']})"},
        {"Metric": "Lowest Scorer", "Value": f"{min_record['name']} ({min_record['score']})"},
    ]
    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Metric", "Value"])
        writer.writeheader()
        writer.writerows(summary_data)
    print(f"\n[Success] Statistical summary exported to '{SUMMARY_CSV}'.")

if __name__ == "__main__":
    process_csv_data()
