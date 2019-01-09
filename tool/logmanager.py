# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import numpy as np

from . import modelmanager
from . import suggestermanager
from .dummy_data import mp2

# toolmanager
from .toolmanager import get_current_classifier
from .toolmanager import get_current_classifier_pickle
from .toolmanager import get_current_measurement_plan
from .toolmanager import set_current_classifier
from .toolmanager import set_current_measurement_plan

def parse_count_log(file):
    with open(file) as f:
        content = f.readlines()
    content = [x[8:].strip() for x in content]
    parsed_content = [ast.literal_eval(x) for x in content]
    return parsed_content

def parse_result_log(file):
    with open(file) as f:
        content = f.readlines()
    result = [x.split('|') for x in content]
    return result

def dummy_export_log(result_log, count_log):
    current_family = modelmanager.save_measurement_plan_family('MP2 Scenario 1')
    mp2_dic = mp2()
    current_measurement_plan = modelmanager.save_measurement_plan_complete(mp2_dic['n_features'], current_family, mp2_dic['classes'], mp2_dic['metrics'], mp2_dic['features'])

    training_file = '/User/dummy/suggester_project/classified_data/001.tr'
    prediction_file = '/User/dummy/suggester_project/predicted_data/001.tr'
    parameters = {
        'kernel': 'rbf',
        'C': 8.0,
        'gamma': 0.125,
        'decision_function_shape': 'ovr',
        'cache_size': 200
    }
    current_svc_model = modelmanager.save_svc_model(training_file, parameters)

    set_current_measurement_plan(current_measurement_plan)
    set_current_classifier(current_svc_model)

    result_log_ = parse_result_log(result_log)
    count_log_ = parse_count_log(count_log)

    for j in range(0, len(result_log_)):
        current_result = result_log_[j]
        current_count = count_log_[j]

        current_file = '%03d' % j
        modelmanager.save_measurement_file('/User/dummy/suggester_project/unclassified_data/' + current_file + 'un', current_measurement_plan, processed=True)
        print current_result[4].strip().encode("ascii")
        suggestion = modelmanager.save_suggestion(current_svc_model, float(current_result[4].strip().encode("ascii")), current_measurement_plan)
        prediction = modelmanager.save_prediction(prediction_file, current_svc_model, current_family)
        for count in current_count:
            modelmanager.save_prediction_frequency(count[0], count[1], prediction)

        measurement_plan_features = current_measurement_plan.get_features_names()
        print current_result[2].strip().encode("ascii")
        selected_features = ast.literal_eval(current_result[2].strip().encode("ascii"))
        selected_features_tuples = []
        for i in selected_features:
            selected_features_tuples.append((i, measurement_plan_features[i]))
        scores = np.random.uniform(0.7, 1, size=len(measurement_plan_features))
        feature_selection = modelmanager.save_feature_selection(suggestion, prediction_file, 10000, len(measurement_plan_features), selected_features_tuples, scores)

        print current_result[3].strip().encode("ascii")
        unnecessary_features = ast.literal_eval(current_result[3].strip().encode("ascii"))
        if len(unnecessary_features) > 0:
            new_mp = suggestermanager.measurement_plan_from_suggestion(
                unnecessary_features, current_measurement_plan)
            suggestion.suggested_measurement_plan_id = new_mp.id
            suggestion.save()
            current_measurement_plan = new_mp
            current_svc_model = modelmanager.save_svc_model(training_file, parameters)
            set_current_measurement_plan(current_measurement_plan)
            set_current_classifier(current_svc_model)
