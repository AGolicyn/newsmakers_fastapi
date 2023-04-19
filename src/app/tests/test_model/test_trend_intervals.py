from app.service.model.model import *

trends = [
    Trend(date=datetime.date(2023, 4, 3), qty=1, source="test-1"),
    Trend(date=datetime.date(2023, 4, 2), qty=2, source="test-2"),
]


def test_make_trend_interval():
    start_day = datetime.date(2023, 4, 3)
    offset = 2

    result = make_trend_interval(trends=trends, start_day=start_day, offset=offset)

    assert len(result) == 2
    for obj in result:
        assert isinstance(obj, DayTrend)
    assert result[0].trends[0].date == datetime.date(2023, 4, 3)
    assert result[0].trends[0].qty == 1
    assert result[0].trends[0].source == "test-1"

    assert result[1].trends[0].date == datetime.date(2023, 4, 2)
    assert result[1].trends[0].qty == 2
    assert result[1].trends[0].source == "test-2"


def test_interval_with_empty_start():
    start_day = datetime.date(2023, 4, 5)
    offset = 4

    result = make_trend_interval(trends=trends, start_day=start_day, offset=offset)

    assert len(result) == 4
    for obj in result:
        assert isinstance(obj, DayTrend)
    assert result[0].trends[0].date == datetime.date(2023, 4, 5)
    assert result[0].trends[0].qty == 0
    assert result[0].trends[0].source == ""

    assert result[2].trends[0].date == datetime.date(2023, 4, 3)
    assert result[2].trends[0].qty == 1
    assert result[2].trends[0].source == "test-1"


def test_interval_with_empty_end():
    start_day = datetime.date(2023, 4, 3)
    offset = 3

    result = make_trend_interval(trends=trends, start_day=start_day, offset=offset)

    assert len(result) == 3
    for obj in result:
        assert isinstance(obj, DayTrend)
    assert result[1].trends[0].date == datetime.date(2023, 4, 2)
    assert result[1].trends[0].qty == 2
    assert result[1].trends[0].source == "test-2"

    assert result[2].trends[0].date == datetime.date(2023, 4, 1)
    assert result[2].trends[0].qty == 0
    assert result[2].trends[0].source == ""


def test_interval_with_empty_body():
    start_day = datetime.date(2023, 4, 2)
    offset = 3
    trends = [
        Trend(date=datetime.date(2023, 4, 2), qty=2, source="test-2"),
        Trend(date=datetime.date(2023, 3, 31), qty=3, source="test-3"),
    ]

    result = make_trend_interval(trends=trends, start_day=start_day, offset=offset)

    assert len(result) == 3
    for obj in result:
        assert isinstance(obj, DayTrend)
    assert result[0].trends[0].date == datetime.date(2023, 4, 2)
    assert result[0].trends[0].qty == 2
    assert result[0].trends[0].source == "test-2"

    assert result[1].trends[0].date == datetime.date(2023, 4, 1)
    assert result[1].trends[0].qty == 0
    assert result[1].trends[0].source == ""

    assert result[2].trends[0].date == datetime.date(2023, 3, 31)
    assert result[2].trends[0].qty == 3
    assert result[2].trends[0].source == "test-3"


def test_interval_empty():
    start_day = datetime.date(2023, 4, 2)
    offset = 3
    trends = []

    result = make_trend_interval(trends=trends, start_day=start_day, offset=offset)

    assert len(result) == 3
    for obj in result:
        assert isinstance(obj, DayTrend)
