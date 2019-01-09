# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import timeit

from collections import Counter

from celery import shared_task

from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file

from . import suggestermanager
from .suggester.dataloader import load_svmlight_instances
from .filemanager import get_new_filename_for_predicted_data
from .filemanager import get_new_filename_for_classified_data
from .modelmanager import save_suggestion
from .modelmanager import save_class_of_interest

# modelmanager
from .modelmanager import next_unprocessed_measurement_file

# suggester
from .suggester.classifier import train_rbf_svm
from .suggester.suggester import Suggester

# toolmanager
from .toolmanager import get_current_classifier
from .toolmanager import get_current_classifier_pickle
from .toolmanager import get_current_measurement_plan
from .toolmanager import set_current_classifier
from .toolmanager import set_current_measurement_plan

def _filter_data_for_measurement_plan(X, source_features, measurement_plan_features):
    indices = []
    i = 0
    for feature in source_features:
        if feature in measurement_plan_features:
            indices.append(i)
        i +=1
    return X[:,indices]

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def model_selection_task(file):
    svc_model = suggestermanager.model_selection(file)
    return svc_model.id

@shared_task
def suggest_task():
    start_time = timeit.default_timer()
    current_svc_model = get_current_classifier()
    current_measurement_plan = get_current_measurement_plan()
    if current_svc_model == None or current_measurement_plan == None:
        return
    print 'suggest_task: mp id ', current_measurement_plan.id
    print 'suggest_task: svcm id ', current_svc_model.id
    
    measurement_file = next_unprocessed_measurement_file(current_measurement_plan.family.id)
    if measurement_file == None:
        return
    print 'suggest_task: next file ', measurement_file.location

    suggester = Suggester()
    suggester.classifier_model = current_svc_model
    suggester.measurement_plan = current_measurement_plan
    X, y = load_svmlight_file(suggester.classifier_model.training_file)
    suggester.classifier = train_rbf_svm(X, y, suggester.classifier_model.C, 
        suggester.classifier_model.gamma)
    print 'suggest_task: svm ', str(suggester.classifier)

    measurement_file_features = measurement_file.measurement_plan.get_features_names()
    measurement_plan_features = current_measurement_plan.get_features_names()
    X = load_svmlight_instances(measurement_file.location)
    X = _filter_data_for_measurement_plan(X, measurement_file_features, measurement_plan_features)
    print 'suggest_task: filter ', str(X.shape)

    suggestion = save_suggestion(suggester.classifier_model, 0.0, suggester.measurement_plan) # <---
    y = suggester.predict(X)
    predicted_data_file = get_new_filename_for_predicted_data()
    dump_svmlight_file(X, y, predicted_data_file)
    prediction_counter = Counter(y) # <---
    print 'suggest_task: predictions ', prediction_counter.most_common()

  #  save_class_of_interest(prediction_counter[0][X], getClasses().get

    fs = suggestermanager.feature_selection(suggestion, predicted_data_file, measurement_plan_features) # <---
    unnecessary_features = suggester.suggest_features_to_remove(suggester.measurement_plan, fs)
    print 'suggest_tak: unnecessary features', unnecessary_features

    if len(unnecessary_features) > 0:
        new_mp = suggestermanager.measurement_plan_from_suggestion(
            unnecessary_features, suggester.measurement_plan)
        X, y = load_svmlight_file(suggester.classifier_model.training_file)
        X = _filter_data_for_measurement_plan(X, current_measurement_plan.get_features_names(), new_mp.get_features_names())
        new_training_file = get_new_filename_for_classified_data()
        dump_svmlight_file(X, y, new_training_file)
        svc_model = suggestermanager.model_selection(new_training_file)
        set_current_measurement_plan(new_mp)
        set_current_classifier(svc_model)

    measurement_file.processed = True
    measurement_file.save()
    elapsed = timeit.default_timer() - start_time
    suggestion.execution_time = elapsed
    suggestion.save()
