import csv
import json

from part2_engine.growth_engine import (
    mom_growth,
    is_flagged,
    validate_feed,
)


def read_revenue(path,month):
    """Read category revenue from a CSV file."""
    data = {}

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["month"] == month:
                data[row["category"]] = float(row["revenue"])

    return data


def run(month, previous_month_csv, current_month_csv):
    """Run the monthly alert workflow."""

    valid, errors = validate_feed(current_month_csv)

    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    previous_month = "April" if month == "May" else "May"
    previous = read_revenue(previous_month_csv, previous_month)
    current = read_revenue(current_month_csv, month)

    flagged = []
    suppressed = []
    escalated = []

    for category in current:
        if category not in previous:
            continue

        growth = mom_growth(previous[category], current[category])
        status = is_flagged(growth)

        if status == "escalate_exact_boundary":
            escalated.append(category)

        elif status == "flagged":
            flagged.append({
                "category": category,
                "mom_pct": growth,
                "previous_revenue": previous[category],
                "current_revenue": current[category],
            })

    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True,
    )

    drafted = flagged[:3]
    remaining = flagged[3:]

    for item in drafted:
        item["drafted"] = True
        item["message"] = (
            f"{item['category']} changed by "
            f"{item['mom_pct']}% MoM."
        )

    for item in remaining:
        suppressed.append(item["category"])

    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }


if __name__ == "__main__":
    result = run(
        "May",
        "part2_engine/fixtures/monthly_category_revenue.csv",
        "part2_engine/fixtures/monthly_category_revenue.csv",
    )

    print(json.dumps(result, indent=2))