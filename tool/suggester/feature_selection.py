# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import sys

from collections import Counter
from sklearn.datasets import load_svmlight_file

from classifier import select_linear_svm_model
from suggester import feature_selection

if __name__=='__main__':
    try:
        # Get file name.
        file = sys.argv[1]
        # Get scenario
        scenario = sys.argv[2]
        # Load classified data
        X, y = load_svmlight_file(file)
        # Count the instances of each class
        counter = Counter(y)
        # Get class of interest.
        labels = []

        if scenario == 'hvrest':
            label, _ = counter.most_common()[0]
            labels.append(label)

        if scenario == 'lvrest':
            label, _ = counter.most_common()[-1]
            labels.append(label)

        # Class of interest vs Rest
        y_bin = map(lambda x: 1 if x in labels else -1, y)
        linear_svm = select_linear_svm_model(X, y_bin)
        features, mask, scores = feature_selection(X, y_bin, linear_svm)
        result = {
            'features': features.tolist(),
            'mask': mask.tolist(),
            'scores': scores.tolist(),
            'n_samples': X.shape[0],
            'n_features': X.shape[1]
        }
    except Exception as e:
        result = {}
    print json.dumps(result)
