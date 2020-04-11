from .globals import CNB_RATES_URL, CNB_TIME_UPDATE

from requests import get
from json import load, dump
from os.path import exists
from datetime import datetime, timedelta


class CachedSource(object):
    """
    Class handling source data and their caching
    """
    _cache_name = "rates_cache"

    def __init__(self, cache_path=""):
        """
        :param cache_path: path to store cache file
        """
        self._cache_path = cache_path
        self.cache_data = None

    def get_rates(self):
        """
        :return: dict with rates
        """
        self.reload_cache()
        return self.cache_data

    def _update_cache(self):
        """
        Updates rates from CNB and stores to cache
        :return: dict with rates
        """
        response = get(CNB_RATES_URL)
        data = self._parse_response(response.text)
        self._store_cache(data)
        return data

    @staticmethod
    def _cnb_update_time():
        """
        Compares current time with time when CNB updates rates
        :return: boolean if update time already was
        """
        time_now = datetime.now().time()
        time_cnb = datetime.strptime(CNB_TIME_UPDATE, '%H:%M').time()
        return time_now > time_cnb

    @classmethod
    def _date_stamp(cls):
        """
        Generates stamp presented in CNB response with rates
        :return: date string in CNB response format
        """
        date_time = datetime.now()
        if not cls._cnb_update_time():
            # because CNB updates rates at specific time
            date_time -= timedelta(days=1)
        return date_time.strftime("%d %b %Y")

    def reload_cache(self):
        """
        If needed reload the cache with current data from CNB and store on class
        """
        if not self.cache_data and self.have_cache():
            self.cache_data = self._load_cache()
        if not self.cache_data or self._date_stamp() not in self.cache_data.get("last_update", ""):
            self.cache_data = self._update_cache()

    def have_cache(self):
        """
        Checks if we have cache presented
        :return: boolean if cache file exists
        """
        return exists(self._cache_path + self._cache_name)

    def _store_cache(self, data):
        """
        Store rates data to cache file
        :param data: dict of rates from CNB
        """
        with open(self._cache_path + self._cache_name, 'w') as json_file:
            dump(data, json_file)

    def _load_cache(self):
        """
        Loads cached data
        :return: dict of rates
        """
        with open(self._cache_path + self._cache_name) as f:
            data = load(f)
        return data

    @staticmethod
    def _parse_response(response):
        """
        Parses the response from CNB endpoint
        :param response: text response from CNB endpoint
        :return: dict of last update date and rates
        """
        lines = response.strip().split("\n")
        last_update = lines.pop(0)
        lines.pop(0)  # we don't need the description line
        rates = {}
        for line in lines:
            # parse the lines and get needed data
            _, _, _, code, rate = line.split("|")
            # store rates
            rates[code] = float(rate)
        return {"last_update": last_update, "rates": rates}



