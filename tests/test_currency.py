from src.currency import Currency
from src.exceptions import UnknownCurrency
from .globals import TEST_RATES

from unittest import TestCase


class TestCurrency(TestCase):
    def test_identify_currency(self):
        # test if currency identification works
        currency = Currency(rates=TEST_RATES["rates"])
        assert currency._identify_currency("€")
        assert currency._identify_currency("$")
        assert currency._identify_currency("AUD")
        with self.assertRaises(UnknownCurrency):
            currency._identify_currency("^")

    def test_currency_to_crows(self):
        # test if we can convert to CZK
        currency = Currency(rates=TEST_RATES["rates"])
        assert currency.crowns_to_currency(15, "AUD") == 1.0
        assert currency.crowns_to_currency(15, "USD") == 1.5

    def test_currency_convert(self):
        # test if we convert it right
        currency = Currency(rates=TEST_RATES["rates"])

        convert = currency.convert(16, "AUD", "USD")
        assert convert["USD"] == 24.0

        convert = currency.convert(16, "CZK", "CZK")
        assert convert["CZK"] == 16

        convert = currency.convert(16, "CZK")
        assert len(convert) == 2

        convert = currency.convert(16, "CZK", json_resp=True)
        assert "input" in convert
        assert "output" in convert

