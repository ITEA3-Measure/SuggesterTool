# Dummy data, for tests. Delete later.

MP2_CLASSES = [
    {
        'label': 1,
        'name': 'Maintainability'
    },
    {
        'label': 2,
        'name': 'System Performance'
    },
    {
        'label': 3,
        'name': 'Performance'
    },
    {
        'label': 4,
        'name': 'Functionality'
    }
]

MP2_METRICS = [
    {
        'name': 'Cognitive Complexity',
        'class': 1
    },
    {
        'name': 'Maintainability Index',
        'class': 1
    },
    {
        'name': 'Code Size',
        'class': 1
    },
    {
        'name': 'No. Bugs',
        'class': 3
    },
    {
        'name': 'Response Time',
        'class': 3
    },
    {
        'name': 'Running Time',
        'class': 3
    },
    {
        'name': 'Usability',
        'class': 4
    },
    {
        'name': 'Computational Cost',
        'class': 2
    },
    {
        'name': 'Infrastructure Cost',
        'class': 2
    },
    {
        'name': 'Communication Cost',
        'class': 2
    },
    {
        'name': 'Tasks',
        'class': 2
    },
    {
        'name': 'I/O Related Errors',
        'class': 3
    },
    {
        'name': 'Precision',
        'class': 4
    },
    {
        'name': 'Stability of Response Time',
        'class': 4
    },
    {
        'name': 'Illegal Operations',
        'class': 4
    }
]

MP2_FEATURES = [
    {
        'index': 0,
        'mandatory': False,
        'metric': 'Cognitive Complexity',
        'name': 'Cognitive Complexity'
    },
    {
        'index': 1,
        'mandatory': True,
        'metric': 'Maintainability Index',
        'name': 'Maintainability Index'
    },
    {
        'index': 2,
        'mandatory': False,
        'metric': 'Code Size',
        'name': 'Code Size'
    },
    {
        'index': 3,
        'mandatory': False,
        'metric': 'No. Bugs',
        'name': 'No. Bugs'
    },
    {
        'index': 4,
        'mandatory': True,
        'metric': 'Response Time',
        'name': 'Response Time'
    },
    {
        'index': 5,
        'mandatory': True,
        'metric': 'Running Time',
        'name': 'Running Time'
    },
    {
        'index': 6,
        'mandatory': True,
        'metric': 'Usability',
        'name': 'Usability'
    },
    {
        'index': 7,
        'mandatory': True,
        'metric': 'Computational Cost',
        'name': 'Computational Cost'
    },
    {
        'index': 8,
        'mandatory': False,
        'metric': 'Infrastructure Cost',
        'name': 'Infrastructure Cost'
    },
    {
        'index': 9,
        'mandatory': False,
        'metric': 'Communication Cost',
        'name': 'Communication Cost'
    },
    {
        'index': 10,
        'mandatory': False,
        'metric': 'Tasks',
        'name': 'Tasks'
    },
    {
        'index': 11,
        'mandatory': False,
        'metric': 'I/O Related Errors',
        'name': 'I/O Related Errors'
    },
    {
        'index': 12,
        'mandatory': False,
        'metric': 'Precision',
        'name': 'Precision'
    },
    {
        'index': 13,
        'mandatory': False,
        'metric': 'Stability of Response Time',
        'name': 'Stability of Response Time'
    },
    {
        'index': 14,
        'mandatory': False,
        'metric': 'Illegal Operations',
        'name': 'Illegal Operations'
    }
]

def mp2():
    mp2 = {
        'n_features': 15,
        'classes': MP2_CLASSES,
        'metrics': MP2_METRICS,
        'features': MP2_FEATURES
    }
    return mp2

def mp2_json():
    import json
    mp2 = {
        'n_features': 15,
        'classes': MP2_CLASSES,
        'metrics': MP2_METRICS,
        'features': MP2_FEATURES
    }
    print json.dumps(mp2)
