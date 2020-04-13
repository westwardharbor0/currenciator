from .exceptions import UnknownCurrency
from .globals import CURRENCIES_SYMBOLS


class Currency(object):
    """
    Class handling the converting
    """
    def __init__(self, rates={}):
        """
        :param rates: loaded rates of currencies from CNB
        """
        self._rates = rates

    def convert(self, amount, convert_from, convert_to=None, json_resp=False):
        """
        Converts amount from given currency to given output
        :param amount: money to convert
        :param convert_from: code or symbol of currency to convert from
        :param convert_to: optional code or symbol of currency to convert to
        :param json_resp: boolean if full json response will be returned
        :return: dict of rates
        """
        c_from = self._identify_currency(convert_from)
        amount_czk = amount * self._rates.get(c_from, 1)
        response = {}
        if convert_to:
            # if we have a currency to convert to
            c_to = self._identify_currency(convert_to)
            response[convert_to] = self.crowns_to_currency(amount_czk, c_to)
        else:
            rates = self._rates.copy()
            rates["CZK"] = 1  # because CZK is not is list, we are in czech republic
            # if we convert to all currencies
            for currency in rates.keys():
                if currency == c_from:
                    # don't return source currency
                    continue
                response[currency] = self.crowns_to_currency(amount_czk, currency)
        if json_resp:
            # returns the full response with input / output data
            return self._json_response(amount, c_from, response)
        return response

    @staticmethod
    def _json_response(amount, convert_from, response):
        """
        Creates the desired full response with input / output data
        :param amount: money to convert
        :param convert_from: currency to convert from
        :param response: currency(ies) to convert to
        :return: dict with response
        """
        return {
            "input": {
                "amount": amount,
                "currency": convert_from
            },
            "output": response
        }

    @staticmethod
    def _identify_currency(currency):
        """
        Translates symbol to currency code if needed
        :param currency: code or symbol of currency
        :return: currency code
        """
        k = list(CURRENCIES_SYMBOLS.keys())
        v = list(CURRENCIES_SYMBOLS.values())
        if currency in k:
            # if currency is code we don't need to translate
            return currency
        if currency in v:
            # if symbol found in translate table return associated code
            return k[v.index(currency)]
        raise UnknownCurrency(currency)

    def crowns_to_currency(self, amount, currency):
        """
        Convert the amount in currency to base (crowns, since we use CNB)
        :param amount: money to convert
        :param currency: currency to convert from to CZK
        :return: amount in CZK
        """
        rate = self._rates.get(currency, 1)
        return round(amount / rate, 2)
