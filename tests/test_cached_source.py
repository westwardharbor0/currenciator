from src.cached_source import CachedSource
from .globals import TEST_RESPONSE_TEXT, TEST_RESPONSE_UPDATE_DATE

from datetime import timedelta, datetime
from unittest import TestCase


class CustomCachedSource(CachedSource):
    """
    Version of CachedSource class to fit the test env
    """
    _cache_name = "test_rates_cache"
    cache_data = None
    _cache_path = "tests/"

    def __init__(self):
        pass

    def _update_cache(self):
        return self._load_cache()


class TestCachedSource(TestCase):
    def test_have_cache(self):
        # test if can determinate presence of cache file
        cache = CustomCachedSource()
        assert cache.have_cache()
        cache._cache_name = "nope_rates_cache"
        assert not cache.have_cache()

    def test_cnb_response_parse(self):
        # test if we are able to parse CNB response
        # it could change
        cache = CustomCachedSource()
        data = cache._parse_response(TEST_RESPONSE_TEXT)
        assert data["last_update"] == TEST_RESPONSE_UPDATE_DATE
        assert len(data["rates"]) == 2

    def test_update_cnb_time(self):
        # test if we can update when the time comes
        cached = CustomCachedSource()
        old_time = (datetime.now() + timedelta(minutes=1)).strftime('%H:%M')
        updated_time = (datetime.now() - timedelta(minutes=1)).strftime('%H:%M')
        assert not cached._cnb_update_time(update_time=old_time)
        assert cached._cnb_update_time(update_time=updated_time)

    def test_get_rates(self):
        cached = CustomCachedSource()
        data = cached.get_rates()
        assert data["last_update"] == TEST_RESPONSE_UPDATE_DATE
        assert len(data["rates"]) == 2
