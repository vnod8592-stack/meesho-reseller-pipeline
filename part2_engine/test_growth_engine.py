from part2_engine.growth_engine import (
    mom_growth,
    is_flagged,
    validate_feed,
)


def test_mom_growth():
    assert mom_growth(100, 120) == 20.0
    assert mom_growth(200, 150) == -25.0


def test_is_flagged():
    assert is_flagged(10) == "flagged"
    assert is_flagged(-10) == "flagged"
    assert is_flagged(5) == "not_flagged"
    assert is_flagged(8) == "escalate_exact_boundary"
    assert is_flagged(-8) == "escalate_exact_boundary"


def test_good_feed():
    valid, errors = validate_feed(
        "part2_engine/fixtures/monthly_category_revenue.csv"
    )

    assert valid is True
    assert errors == []


def test_corrupted_feed():
    valid, errors = validate_feed(
        "part2_engine/fixtures/corrupted_feed.csv"
    )

    assert valid is False
    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]