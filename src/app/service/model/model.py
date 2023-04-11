import datetime
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass()
class Trend:
    date: datetime.date
    qty: int
    source: str


@dataclass()
class WeightTrend:
    date: datetime.date
    weight: float


def trend_calculator(all_sources: list[str],
                     trends: list[Trend],
                     start_day: datetime.date,
                     offset: int) -> list[WeightTrend]:
    result = make_trend_interval(trends=trends, start_day=start_day, offset=offset)
    trend_line = TrandLine(sources=all_sources, trends=result)
    return trend_line.get_weighted_trends()


class DayTrend:
    """Класс агрегирующий тренды одного дня"""

    def __init__(self, trends: list[Trend]):
        self._check_valid_dates(trends)
        self.trend_day = trends[0].date
        self.trends = trends

    def __repr__(self):
        res = ''
        for trnd in self.trends:
            res += f"{trnd.date} {trnd.source} {trnd.qty}\n"
        res += '\n'
        return res

    def __len__(self):
        if not self.trends[0].source:
            return 0
        return len(self.trends)

    def get_token_quantity(self):
        summa = 0
        for trend in self.trends:
            summa += trend.qty
        return summa

    @staticmethod
    def _check_valid_dates(trends: list[Trend]):
        valid_date = trends[0].date
        if any([trend for trend in trends if trend.date != valid_date]):
            raise ValueError('Trends dates should be equal')


class TrandLine:
    """Класс для обаботки коллекции дневных трендов"""

    def __init__(self, sources: Sequence, trends: list[DayTrend]):
        self.interval_trends = trends
        self.sources = sources

    def _count_weights(self, k1: float, k2: float):
        w1_weights = []
        w2_weights = []
        source_qty = len(self.sources)
        for trend in self.interval_trends:
            # Доля газет в которых есть токен, по отношению к общему кол-ву газет
            w1 = len(trend) / source_qty
            w1_weights.append(w1)
            # Частота появления токена
            w2_weights.append(trend.get_token_quantity())

        w2_weights = [qty * 0.01 for qty in w2_weights]
        print(w1_weights)
        print(w2_weights)
        return list(
            [
                WeightTrend(date=trend.trend_day, weight=round(k1 * w1 + k2 * w2, 2))
                for w1, w2, trend in
                zip(w1_weights, w2_weights, self.interval_trends)
            ]
        )

    def get_weighted_trends(self) -> list[WeightTrend]:
        return self._count_weights(k1=0.6, k2=0.4)


def make_trend_interval(trends: list[Trend],
                        start_day: datetime.date,
                        offset: int) -> list[DayTrend]:

    target_day = start_day - datetime.timedelta(days=offset)
    current = start_day
    exists_current = trends[0].date if trends else target_day
    result = []

    while current > exists_current:
        result.append(DayTrend([Trend(date=current, qty=0, source='')]))
        current -= datetime.timedelta(days=1)

    i = 0
    temp = []
    while current > target_day:
        if i < len(trends) and trends[i].date == current:
            temp.append(trends[i])
            i += 1
        else:
            if temp:
                result.append(DayTrend(temp))
                temp = []
            else:
                result.append(DayTrend([Trend(date=current, qty=0, source='')]))
            current -= datetime.timedelta(days=1)

    while current > target_day:
        result.append(DayTrend([Trend(date=current, qty=0, source='')]))
        current -= datetime.timedelta(days=1)

    return result
