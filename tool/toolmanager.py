# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading

from . import cachemanager
from .modelmanager import get_measurement_plan
from .modelmanager import get_svc_model

measurement_plan_lock = threading.Lock()
classifier_lock = threading.Lock()

CURRENT_CLASSIFIER_KEY = 'current_classifier_id'
CURRENT_CLASSIFIER_PICKLE_KEY = 'current_classifier_pickle'
CURRENT_MEASUREMENT_PLAN_KEY = 'current_measurement_plan_id'

def _get(lock, key):
    try:
        lock.acquire()
        return cachemanager.get_from_cache(key)
    finally:
        lock.release()

def _set(lock, key, value):
    try:
        lock.acquire()
        cachemanager.set_to_cache(key, value)
    finally:
        lock.release()

def get_current_classifier():
    global classifier_lock
    current_classifier_id = _get(classifier_lock, CURRENT_CLASSIFIER_KEY)
    print(current_classifier_id)
    if current_classifier_id == None:
            return None
    else:
        classifier = get_svc_model(current_classifier_id)
        return classifier

def set_current_classifier(svc_model):
    global classifier_lock
    _set(classifier_lock, CURRENT_CLASSIFIER_KEY, svc_model.id)

def get_current_classifier_pickle():
    global classifier_lock
    return _get(classifier_lock, CURRENT_CLASSIFIER_PICKLE_KEY)

def set_current_classifier_pickle(classifier_pickle):
    global classifier_lock
    _set(classifier_lock, CURRENT_CLASSIFIER_PICKLE_KEY, classifier_pickle)

def get_current_measurement_plan():
    global measurement_plan_lock
    current_measurement_plan_id = _get(measurement_plan_lock, CURRENT_MEASUREMENT_PLAN_KEY)
    print(current_measurement_plan_id)
    if current_measurement_plan_id == None:
        return None
    mp = get_measurement_plan(current_measurement_plan_id)
    return mp

def set_current_measurement_plan(measurement_plan):
    global measurement_plan_lock
    _set(measurement_plan_lock, CURRENT_MEASUREMENT_PLAN_KEY, measurement_plan.id)
