import datetime
from unittest import TestCase

from issues.time_deltas import TimeDeltas


class TestTimeDeltas(TestCase):
    def test_time_deltas_shortest(self):
        """
        Test the TimeDeltas.shortest method.
        """
        timedeltas = TimeDeltas([])
        self.assertIsNone(timedeltas.shortest)
        timedeltas.times = [
            datetime.timedelta(seconds=10),
            datetime.timedelta(seconds=20),
            datetime.timedelta(hours=15),
        ]
        self.assertEqual(timedeltas.shortest, datetime.timedelta(seconds=10))
        timedeltas.times = [
            datetime.timedelta(hours=5),
            datetime.timedelta(seconds=60),
            datetime.timedelta(seconds=15),
        ]
        self.assertEqual(timedeltas.shortest, datetime.timedelta(seconds=15))

    def test_time_deltas_longest(self):
        """
        Test the TimeDeltas.longest method.
        """
        timedeltas = TimeDeltas([])
        self.assertIsNone(timedeltas.longest)
        timedeltas.times = [
            datetime.timedelta(seconds=10),
            datetime.timedelta(seconds=20),
            datetime.timedelta(hours=15),
        ]
        self.assertEqual(timedeltas.longest, datetime.timedelta(hours=15))
        timedeltas.times = [
            datetime.timedelta(hours=5),
            datetime.timedelta(seconds=60),
            datetime.timedelta(seconds=15),
        ]
        self.assertEqual(timedeltas.longest, datetime.timedelta(hours=5))

    def test_time_deltas_avg(self):
        """
        Test the TimeDeltas.avg method.
        """
        timedeltas = TimeDeltas([])
        self.assertIsNone(timedeltas.avg)
        timedeltas.times = [datetime.timedelta(seconds=10), datetime.timedelta(seconds=20)]
        self.assertEqual(timedeltas.avg, datetime.timedelta(seconds=15))
        timedeltas.times = [
            datetime.timedelta(hours=1),
            datetime.timedelta(hours=2),
            datetime.timedelta(hours=3),
        ]
        self.assertEqual(timedeltas.avg, datetime.timedelta(hours=2))
