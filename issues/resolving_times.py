from __future__ import annotations

import dataclasses
import datetime


@dataclasses.dataclass
class TimeDeltas:
    """
    A list of `datetime.timedelta`s and tools for working with it.
    """

    times: list[datetime.timedelta]

    @property
    def shortest(self) -> datetime.timedelta | None:
        return min(self.times) if self.times else None

    @property
    def longest(self) -> datetime.timedelta | None:
        return max(self.times) if self.times else None

    @property
    def avg(self) -> datetime.timedelta | None:
        if not self.times:
            return None
        return datetime.timedelta(
            seconds=round(sum(t.total_seconds() for t in self.times) / len(self.times))
        )
