# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .modelmanager import save_feature_selection
from .modelmanager import save_model_selection
from .modelmanager import save_svc_model
from .modelmanager import save_measurement_plan_complete
from .suggester.suggester import Suggester

# Methods to manage tool's suggester.

def feature_selection(suggestion, file, features, scenario='hvrest'):
    suggester = Suggester()
    selected_features, mask, scores, n_samples, n_features = suggester.feature_selection(file, scenario)
    selected_features_tuples = []
    i = 0
    for value in mask:
        if value:
            selected_features_tuples.append((i, features[i]))
        i += 1
    fs = save_feature_selection(suggestion, file, n_samples, n_features, selected_features_tuples, scores)
    return fs

def model_selection(file):
    suggester = Suggester()
    best_params, best_score, C_range, gamma_range, scores = suggester.select_rbf_svm(file)
    svc = save_svc_model(file, best_params)
    save_model_selection(svc, best_score, gamma_range, C_range, scores)
    return svc

def measurement_plan_from_suggestion(unnecessary_features, mp):
    n_features = mp.n_features - len(unnecessary_features)
    classes = []
    for c in mp.get_classes():
        dic = {
            'label': c.label, 
            'name': c.name
        }
        classes.append(dic)
    new_metrics_set = set()
    features = []
    i = 0
    j = 0
    for f in mp.get_features():
        if i in unnecessary_features:
            pass
        else:
            dic = { 'index': j, 'name': f.name, 'mandatory': f.mandatory, 'metric': f.metric.name }
            new_metrics_set.add(f.metric.name)
            features.append(dic)
            j += 1
        i += 1
    metrics = []
    for m in mp.get_metrics():
        if m.name in new_metrics_set:
            dic = {'name': m.name, 'class': m.measurement_plan_class.label}
            metrics.append(dic)
    new_mp = save_measurement_plan_complete(n_features, mp.family, classes, metrics, features, mp)
    return new_mp
