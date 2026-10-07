from typing import List, Dict, Any, Optional
from collections import defaultdict
from datetime import datetime
import calendar
from .expense import Expense
from .utils import format_currency, render_ascii_bar

class ReportGenerator:
    @staticmethod
    def generate_monthly_summary(
        expenses: List[Expense],
        year: int,
        month: int,
        budget: Optional[float] = None
    ) -> Dict[str, Any]:
        month_prefix = f"{year:04d}-{month:02d}"
        month_expenses = [e for e in expenses if e.date.startswith(month_prefix)]
        month_name = calendar.month_name[month]
        num_days = calendar.monthrange(year, month)[1]

        total_spent = sum(e.amount for e in month_expenses)
        tx_count = len(month_expenses)

        avg_per_day = round(total_spent / num_days, 2) if num_days > 0 else 0.0

        highest_exp = max(month_expenses, key=lambda x: x.amount) if month_expenses else None
        lowest_exp = min(month_expenses, key=lambda x: x.amount) if month_expenses else None

        cat_map = defaultdict(float)
        for e in month_expenses:
            cat_map[e.category] += e.amount

        category_breakdown = []
        for cat, amt in sorted(cat_map.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / total_spent * 100.0) if total_spent > 0 else 0.0
            category_breakdown.append({
                "category": cat,
                "amount": round(amt, 2),
                "percentage": round(pct, 1),
                "bar": render_ascii_bar(pct, width=15)
            })

        budget_info = None
        if budget is not None and budget > 0:
            remaining = budget - total_spent
            pct_used = (total_spent / budget * 100.0)
            is_over = total_spent > budget
            budget_info = {
                "budget_amount": budget,
                "remaining": round(remaining, 2),
                "percentage_used": round(pct_used, 1),
                "is_over": is_over,
                "bar": render_ascii_bar(pct_used, width=15)
            }

        return {
            "year": year,
            "month": month,
            "month_name": month_name,
            "total_spent": round(total_spent, 2),
            "transaction_count": tx_count,
            "average_per_day": avg_per_day,
            "highest_expense": highest_exp,
            "lowest_expense": lowest_exp,
            "categories": category_breakdown,
            "budget_info": budget_info
        }

    @staticmethod
    def generate_category_breakdown(expenses: List[Expense]) -> List[Dict[str, Any]]:
        if not expenses:
            return []

        total_spent = sum(e.amount for e in expenses)
        cat_map = defaultdict(lambda: {"amount": 0.0, "count": 0})

        for e in expenses:
            cat_map[e.category]["amount"] += e.amount
            cat_map[e.category]["count"] += 1

        breakdown = []
        for cat, data in sorted(cat_map.items(), key=lambda x: x[1]["amount"], reverse=True):
            amt = data["amount"]
            pct = (amt / total_spent * 100.0) if total_spent > 0 else 0.0
            breakdown.append({
                "category": cat,
                "amount": round(amt, 2),
                "count": data["count"],
                "percentage": round(pct, 1),
                "bar": render_ascii_bar(pct, width=20)
            })

        return breakdown

    @staticmethod
    def generate_trend_analysis(expenses: List[Expense], max_months: int = 6) -> List[Dict[str, Any]]:
        if not expenses:
            return []

        monthly_totals = defaultdict(float)
        for e in expenses:
            month_key = e.date[:7]
            monthly_totals[month_key] += e.amount

        sorted_months = sorted(monthly_totals.keys())[-max_months:]
        max_month_val = max([monthly_totals[m] for m in sorted_months], default=1.0) or 1.0

        trends = []
        prev_amt = None
        for m in sorted_months:
            amt = monthly_totals[m]
            pct_of_max = (amt / max_month_val * 100.0)
            chg_pct = None
            if prev_amt is not None and prev_amt > 0:
                chg_pct = round(((amt - prev_amt) / prev_amt) * 100.0, 1)

            trends.append({
                "month_key": m,
                "amount": round(amt, 2),
                "bar": render_ascii_bar(pct_of_max, width=15),
                "change_percentage": chg_pct
            })
            prev_amt = amt

        return trends

    @staticmethod
    def predict_month_end(expenses: List[Expense], year: int, month: int) -> Dict[str, Any]:
        now = datetime.now()
        month_prefix = f"{year:04d}-{month:02d}"
        month_expenses = [e for e in expenses if e.date.startswith(month_prefix)]
        total_so_far = sum(e.amount for e in month_expenses)
        total_days = calendar.monthrange(year, month)[1]

        if year == now.year and month == now.month:
            days_elapsed = max(1, now.day)
        elif (year < now.year) or (year == now.year and month < now.month):
            days_elapsed = total_days
        else:
            days_elapsed = 1

        daily_rate = total_so_far / days_elapsed
        projected_total = daily_rate * total_days

        return {
            "year": year,
            "month": month,
            "days_elapsed": days_elapsed,
            "total_days": total_days,
            "total_so_far": round(total_so_far, 2),
            "daily_run_rate": round(daily_rate, 2),
            "projected_total": round(projected_total, 2)
        }

    @classmethod
    def format_monthly_report_text(cls, summary: Dict[str, Any]) -> str:
        lines = []
        lines.append("=" * 65)
        title = f"MONTHLY EXPENSE REPORT: {summary['month_name']} {summary['year']}"
        lines.append(title.center(65))
        lines.append("=" * 65)
        lines.append(f"Total Expenditure  : {format_currency(summary['total_spent'])}")
        lines.append(f"Total Transactions : {summary['transaction_count']}")
        lines.append(f"Average Daily Spend: {format_currency(summary['average_per_day'])}")

        if summary['highest_expense']:
            h = summary['highest_expense']
            lines.append(f"Highest Expense    : {format_currency(h.amount)} ({h.category} - {h.description})")
        if summary['lowest_expense']:
            l = summary['lowest_expense']
            lines.append(f"Lowest Expense     : {format_currency(l.amount)} ({l.category} - {l.description})")

        if summary.get("budget_info"):
            b = summary["budget_info"]
            lines.append("-" * 65)
            lines.append("BUDGET TRACKING:")
            lines.append(f"  Allocated Budget : {format_currency(b['budget_amount'])}")
            lines.append(f"  Remaining Budget : {format_currency(b['remaining'])}")
            lines.append(f"  Budget Used      : {b['bar']}")
            if b['is_over']:
                lines.append(f"  [ALERT] OVER BUDGET BY {format_currency(abs(b['remaining']))}!")
            elif b['percentage_used'] >= 80:
                lines.append("  [WARNING] You have consumed over 80% of your budget!")

        lines.append("-" * 65)
        lines.append("CATEGORY BREAKDOWN:")
        if not summary['categories']:
            lines.append("  No recorded expenses for this period.")
        else:
            lines.append(f"  {'Category':<22} {'Amount':>10}  {'Visual Share':<25}")
            lines.append("  " + "-" * 60)
            for c in summary['categories']:
                lines.append(f"  {c['category']:<22} {format_currency(c['amount']):>10}  {c['bar']}")

        lines.append("=" * 65)
        return "\n".join(lines)
