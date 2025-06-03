import datetime
import statistics
import unittest
from unittest.mock import MagicMock

from site_manager.stats import get_average_age, get_deals_count


# Create your tests here.
class TestGetDealsCount(unittest.TestCase):

    def test_normal_deals(self):
        deals = [
            MagicMock(realty=MagicMock(price=100000)),
            MagicMock(realty=MagicMock(price=0)),
            MagicMock(realty=MagicMock(price=250000))
        ]
        self.assertEqual(get_deals_count(deals), 350000)

    def test_empty_deals(self):
        self.assertEqual(get_deals_count([]), 0)

    def test_deals_with_missing_realty_or_price(self):
        deals = [
            MagicMock(realty=None),  # нет realty
            MagicMock(realty=MagicMock(price=None)),  # цена отсутствует
            MagicMock(realty=MagicMock(price=200000))
        ]
        self.assertEqual(get_deals_count(deals), 200000)

    def test_deals_with_negative_price(self):
        deals = [
            MagicMock(realty=MagicMock(price=-100000)),
            MagicMock(realty=MagicMock(price=50000))
        ]
        self.assertEqual(get_deals_count(deals), -50000)


class TestGetAverageAge(unittest.TestCase):

    def test_normal_ages(self):
        year = datetime.date.today().year
        peoples = [
            MagicMock(user=MagicMock(birth_day=datetime.date(year - 20, 5, 1))),
            MagicMock(user=MagicMock(birth_day=datetime.date(year - 30, 7, 1))),
            MagicMock(user=MagicMock(birth_day=datetime.date(year - 40, 1, 1)))
        ]
        self.assertEqual(get_average_age(peoples), 30)

    def test_user_with_future_birthdate_ignored(self):
        future_year = datetime.date.today().year + 5
        peoples = [
            MagicMock(user=MagicMock(birth_day=datetime.date(future_year, 1, 1))),  # игнорируется
            MagicMock(user=MagicMock(birth_day=datetime.date(datetime.date.today().year - 25, 1, 1)))
        ]
        self.assertEqual(get_average_age(peoples), 25)

    def test_user_with_missing_birthdate_ignored(self):
        peoples = [
            MagicMock(user=MagicMock(birth_day=None)),
            MagicMock(user=MagicMock(birth_day=datetime.date.today().replace(year=datetime.date.today().year - 40)))
        ]
        self.assertEqual(get_average_age(peoples), 40)

    def test_all_invalid_birthdates_raises(self):
        peoples = [
            MagicMock(user=MagicMock(birth_day=None)),
            MagicMock(user=MagicMock(birth_day=datetime.date.today().replace(year=datetime.date.today().year + 10)))
        ]
        with self.assertRaises(statistics.StatisticsError):
            get_average_age(peoples)

    def test_empty_peoples_raises(self):
        with self.assertRaises(statistics.StatisticsError):
            get_average_age([])
