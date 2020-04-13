from unittest import TestCase
from os import unlink

from src.globals import CURRENCIES_SYMBOLS
from src.currency import Currency
from src.cached_source import CachedSource

TEST_FOLDER = "tests/"
TEST_RATES_NAME = "test_all_rates_cache"


class TestAllCurrencies(TestCase):
    @classmethod
    def tearDownClass(cls):
        # destroy the files we don't need
        unlink(TEST_FOLDER + TEST_RATES_NAME)

    def test_all_currencies(self):
        # get real data
        cached = CachedSource(cache_path=TEST_FOLDER)
        cached._cache_name = TEST_RATES_NAME
        rates_obj = cached.get_rates()
        # prepare currency class
        currency = Currency(rates=rates_obj["rates"])
        # convert all known symbols
        for symbol in CURRENCIES_SYMBOLS.values():
            c = currency.convert(1, "CZK", symbol)
            assert c.get(symbol)
        # convert all known currencies
        for symbol in CURRENCIES_SYMBOLS.keys():
            c = currency.convert(1, "CZK", symbol)
            assert c.get(symbol)
