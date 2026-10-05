import csv


def mom_growth(previous, current):
    """
    Calculate month-over-month percentage growth.
    """
    return round(((current - previous) / previous) * 100, 2)


def is_flagged(mom_pct, threshold=8.0):
    """
    Classify a MoM percentage according to the project threshold.
    """
    if abs(mom_pct) > threshold:
        return "flagged"
    elif abs(mom_pct) < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(path):
    """
    Validate the monthly category revenue feed.

    Returns:
        (True, []) when the feed is valid.
        (False, errors) when problems are found.
    """
    errors = []

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for line_number, row in enumerate(reader, start=2):
            month = row.get("month", "")
            category = row.get("category", "")
            revenue = row.get("revenue", "")

            if not category:
                errors.append(
                    f"line {line_number}: missing category (month={month})"
                )

            if revenue == "":
                errors.append(
                    f"line {line_number}: missing revenue (category={category})"
                )
            else:
                try:
                    revenue_value = float(revenue)

                    if revenue_value < 0:
                        errors.append(
                            f"line {line_number}: negative revenue "
                            f"({revenue_value}) for category={category}"
                        )
                except ValueError:
                    errors.append(
                        f"line {line_number}: invalid revenue "
                        f"({revenue}) for category={category}"
                    )

    return len(errors) == 0, errors