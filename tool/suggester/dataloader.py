# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np
import scipy.sparse as sp

def _dump_svmlight_instances(X, f):
    for i in range(X.shape[0]):
        row = []
        for j in range(X.shape[1]):
            row.append('%d:%f' % (j, X[i,j]))
        row_str = ' '.join(row)
        row_str += '\n'
        f.write(row_str.encode('ascii'))

def dump_svmlight_instances(X, f):
    if hasattr(f, "write"):
        _dump_svmlight_instances(X, f)
    else:
        with open(f, "wb") as f:
            _dump_svmlight_instances(X, f)

def load_svmlight_instances(file):
    """
    Load file without labels.
    """
    data  = []
    indices = []
    indptr = []
    with open(file) as infile:
        data, indices, indptr = _load_svmlight_instances(infile)
    np_data = np.array(data, dtype=np.float64)
    np_indptr = np.array(indptr, dtype=np.intc)
    np_indices = np.array(indices, dtype=np.intc)
    min_idx = np.amin(np_indices)
    max_idx = np.amax(np_indices)
    n_features = (max_idx - min_idx) + 1
    if np.min(np_indices) > 0:
        np_indices -= 1
    shape = (np_indptr.shape[0] - 1, n_features)
    X = sp.csr_matrix((np_data, np_indices, np_indptr), shape)
    return X

def _load_svmlight_instances(f):
    data = []
    indices = []
    indptr = [0]
    for line in f:
        features = line.split()
        n_features = len(features)
        if n_features == 0:
            continue
        for i in range(0, n_features):
            idx_s, value = features[i].split(':', 1)
            indices.append(int(idx_s))
            data.append(float(value))
        indptr.append(len(data))
    return data, indices, indptr
