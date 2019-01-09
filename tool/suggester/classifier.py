# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy

from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.svm  import SVC

def _exponentially_growing_sequences(base, start, stop, step=2, dtype=numpy.float64):
    arange = numpy.arange(start, stop+step, step, dtype)
    sequence = numpy.power(base, arange)
    return sequence

def select_rbf_svm_model(X, y, cv=5, n_jobs=2):
    estimator = SVC()
    C_range = _exponentially_growing_sequences(2, -5, 15)
    gamma_range = _exponentially_growing_sequences(2, -15, 3)
    parameters = {
        'C': C_range,  
        'decision_function_shape': ['ovr'],
        'cache_size': [200.0],
        'kernel': ['rbf'],
        'gamma': gamma_range
    }

    # cv-fold cross validation, use n_jobs thread as each fold and each parameter set can be train in parallel
    grid = GridSearchCV(estimator, param_grid=parameters, cv=cv, n_jobs=n_jobs, verbose=0)
    grid.fit(X, y)
    scores = grid.cv_results_['mean_test_score'].reshape(len(C_range), len(gamma_range))

    return grid.best_params_, grid.best_score_, C_range, gamma_range, scores

def select_linear_svm_model(X, y, cv=10, n_jobs=2):
    base_02_sequence = _exponentially_growing_sequences(2, -5, 15)
    base_10_sequence = _exponentially_growing_sequences(10, -5, 15)
    C_range = numpy.append(base_02_sequence, base_10_sequence)
    C_range = numpy.sort(C_range)
    param_grid = {
        'C': C_range,
        'dual': [True]       
    }
    n_samples, n_features = X.shape
    if n_samples > n_features:
        param_grid['dual'] = [False]
    grid = GridSearchCV(LinearSVC(), param_grid=param_grid, cv=cv, n_jobs=n_jobs, verbose=0)
    grid.fit(X, y)
    return grid.best_estimator_

def train_rbf_svm(X, y, C, gamma, decision_function_shape='ovr', cache_size=200.0):
    svm = SVC(kernel='rbf', C=C, gamma=gamma,
        decision_function_shape=decision_function_shape, cache_size=cache_size)
    svm.fit(X, y)
    return svm
