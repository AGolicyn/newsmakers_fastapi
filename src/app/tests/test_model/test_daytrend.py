import pytest

from app.service.model.model import *


def test_can_create_instance():
    trends = [
        Trend(date=datetime.date(2023, 3, 10), qty=10, source="test-1"),
        Trend(date=datetime.date(2023, 3, 10), qty=11, source="test-2"),
    ]

    obj = DayTrend(trends)

    assert len(obj) == 2
    assert obj.trends[0].date == datetime.date(2023, 3, 10)
    assert obj.trends[0].qty == 10
    assert obj.trends[0].source == "test-1"

    assert obj.trends[1].date == datetime.date(2023, 3, 10)
    assert obj.trends[1].qty == 11
    assert obj.trends[1].source == "test-2"


def test_cant_create_with_different_trend_dates():
    trends = [
        Trend(date=datetime.date(2023, 3, 10), qty=10, source="test-1"),
        Trend(date=datetime.date(2023, 3, 9), qty=11, source="test-2"),
    ]

    with pytest.raises(ValueError, match="Trends dates should be equal"):
        DayTrend(trends)


def test_token_quantity_method():
    trends = [
        Trend(date=datetime.date(2023, 3, 10), qty=10, source="test-1"),
        Trend(date=datetime.date(2023, 3, 10), qty=11, source="test-2"),
    ]

    obj = DayTrend(trends)

    assert obj.get_token_quantity() == 21
