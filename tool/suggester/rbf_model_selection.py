# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import sys

from sklearn.datasets import load_svmlight_file

from classifier import select_rbf_svm_model

if __name__=='__main__':
    try:
        # Get file name.
        file = sys.argv[1]
        # Load classified data
        X, y = load_svmlight_file(file)
        best_params, best_score, C_range, gamma_range, scores = select_rbf_svm_model(X, y)
        result = {
            'best_params': best_params,
            'best_score': best_score,
            'C_range': C_range.tolist(),
            'gamma_range': gamma_range.tolist(),
            'scores': scores.tolist()
        }
    except Exception as e:
        # print str(e)
        result = {}
    print json.dumps(result)
