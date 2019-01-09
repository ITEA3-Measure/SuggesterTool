# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache

def get_from_cache(key):
    return cache.get(key)

def set_to_cache(key, value):
    cache.set(key, value, None)
