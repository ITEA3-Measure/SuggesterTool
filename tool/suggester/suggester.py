# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import expanduser
from os.path import join

import json
import subprocess
import threading

from sklearn.datasets import load_svmlight_file
from sklearn.feature_selection import RFECV

from classifier import train_rbf_svm

USER_PATH = expanduser('~')
SUGGESTER_PATH = join(USER_PATH, 'suggester_tool/tool/suggester')

class Suggester():

    def __init__(self):
        self.classifier = None
        self.classifier_model = None
        self.selected_features = []
        self.measurement_plan = None
        self._classifier_lock = threading.Lock()

    def _prepare_classifier(self):
        if self.classifier == None:
            X, y = load_svmlight_file(self.classifier_model.training_file)
            clf = train_rbf_svm(X, y, self.classifier_model.C, self.classifier_model.gamma)
            self.classifier = clf

    def feature_selection(self, file, scenario):
        try:
            process = subprocess.Popen(
                ['python', 'feature_selection.py', file, scenario],
                cwd=SUGGESTER_PATH, 
                stdout=subprocess.PIPE
            )
            outs, errs = process.communicate()
            clean_out = outs.strip()
            result = json.loads(clean_out)
            return result['features'], result['mask'], result['scores'], result['n_samples'], result['n_features']
        except:
            result = []
        return result

    def predict(self, X):
        try:
            self._classifier_lock.acquire()
            self._prepare_classifier()
            y = self.classifier.predict(X)
        except:
            y = None
        finally:
            self._classifier_lock.release()
        return y

    def select_rbf_svm(self, file):
        try:
            process = subprocess.Popen(
                ['python', 'rbf_model_selection.py', file], 
                cwd=SUGGESTER_PATH,
                stdout=subprocess.PIPE
            )
            outs, errs = process.communicate()
            clean_out = outs.strip()
            result = json.loads(clean_out)
            return result['best_params'], result['best_score'], result['C_range'], result['gamma_range'], result['scores']
        except:
            return {}

    def suggest_features_to_remove(self, measurement_plan, feature_selection):
        measurement_plan_set = set(measurement_plan.get_features_names())
        print measurement_plan_set
        recommended_feature_set = set(feature_selection.get_selected_features_names())
        print recommended_feature_set
        required_feature_set = set(measurement_plan.get_mandatory_features_names())
        print required_feature_set
        difference = measurement_plan_set - recommended_feature_set - required_feature_set
        return list(difference)

def feature_selection(X, y, estimator, cv=5, n_jobs=2):
    """
    Returns a list with the selected features.
    """
    rfecv = RFECV(estimator=estimator, step=1, cv=cv, scoring='accuracy', n_jobs=n_jobs, verbose=0)
    rfecv.fit(X, y)
    features = rfecv.get_support(True)
    mask = rfecv.get_support()
    scores = rfecv.grid_scores_
    return features, mask, scores

