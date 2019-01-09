# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from .models import Feature
from .models import FeatureSelection
from .models import FeatureSelectionScore
from .models import GridSearchScore
from .models import MeasurementFile
from .models import MeasurementPlan
from .models import MeasurementPlanClass
from .models import MeasurementPlanFamily
from .models import Metric
from .models import ModelSelection
from .models import Prediction
from .models import PredictionFrequency
from .models import SelectedFeature
from .models import Suggestion
from .models import SVCModel

# Methods to manage models. (Crete, update, delete ...)

# MeasurementPlanFamily
def get_measurement_plan_family(family_id):
    try:
        family = MeasurementPlanFamily.objects.get(pk=family_id)
        return family
    except MeasurementPlanFamily.DoesNotExist:
        return None

def get_all_families():
    families = list(MeasurementPlanFamily.objects.order_by('id'))
    return families

def save_measurement_plan_family(name):
    family = MeasurementPlanFamily(name=name)
    family.save()
    return family

def get_measurement_plan_family_predictions(family_id):
    # family = get_measurement_plan_family(family_id):
    # if family == None:
    #     return None
    # first_mp = family.get_first_measurement_plan()
    # if first_mp == None:
    #     return None
    # classes = []
    # for c in first_mp.get_classes():
    #     classes.append(list())
    # for p in family.get_predictions():
    #     for f in p.get_frequencies():
    #         classes[f.label - 1].append(frequency)
    classes = [
        [2280, 2518, 2568, 2559, 2579, 2511, 2511, 2568, 2557, 2536, 2589, 2633,
        2562, 2512, 2535, 2523, 2487, 2465, 2540, 2554, 2602, 2509, 2512, 2546,
        2575, 2544, 2575, 2532, 2548, 2539, 2620, 2505, 1903, 1877, 1970, 1837,
        1902, 1908, 1933, 1856, 1903, 1864, 1867, 2120, 2150, 2145, 2161, 2114,
        2121, 2150, 2097, 2093, 2142, 2119, 2147, 2092, 2086, 2109, 2118, 2142,
        2156, 2136, 2159, 2106, 2114, 2176, 2121, 2186, 2137, 2156, 2095, 2107,
        2210, 2119, 2128, 2039, 2217, 2182, 2094, 2028, 2108, 2077, 2158, 2153,
        2147, 2137, 2081, 2132, 2084, 2062, 2163, 2100, 2117, 2109, 2099, 2168,
        2187, 2140, 2130, 2207, 2031, 2096, 2151, 2135, 2162, 2111, 2067, 2099,
        2142, 2139, 2177, 2064, 2154, 2097, 2119, 2117, 2068, 2151, 2105, 2071,
        2187, 2070, 2109, 2144, 2193, 2127, 2149, 2134, 2086, 2135, 2082, 2130,
        2023, 2157, 2121, 2075, 2172, 2114, 2132, 2099, 2114, 2151, 2050, 2092,
        2105, 2118, 2119, 2142, 2225, 2125, 2060, 2082, 2218, 2108, 2126, 2088,
        2104, 2127, 2136, 2105, 2201, 2122, 2147, 2122, 2043, 2132, 2134, 2037,
        2117, 2076, 2132, 2101, 2101, 2126, 2169, 2133, 2190, 2145, 2120, 2101,
        2129, 2131, 2164, 2088, 2122, 2116, 2149, 2172, 2084, 2214, 2156, 2109,
        2110, 2121, 2124, 2079, 2165, 2125, 2060, 2150, 2183, 2037, 2110, 2129,
        2093, 2093, 2113, 2117, 2065, 2153, 2100, 2146, 2093, 2029, 2114, 2070,
        2112, 2112, 2152, 2130, 2148, 2109, 2136, 2127, 2106, 2116, 2057, 2145,
        2202, 2181, 2110, 2036, 2104, 2120, 2134, 2100, 2103, 2081, 2209, 2091],
        [1305, 1389, 1359, 1410, 1328, 1442, 1355, 1390, 1398, 1321, 1356, 1308,
        1387, 1341, 1359, 1381, 1401, 1430, 1419, 1368, 1388, 1377, 1403, 1337,
        1384, 1405, 1376, 1374, 1386, 1370, 1333, 1376, 1733, 1712, 1718, 1740,
        1694, 1754, 1720, 1674, 1697, 1743, 1763, 1377, 1458, 1394, 1419, 1473,
        1390, 1386, 1434, 1417, 1362, 1435, 1461, 1456, 1423, 1358, 1378, 1415,
        1428, 1387, 1392, 1400, 1339, 1419, 1385, 1401, 1359, 1375, 1409, 1391,
        1348, 1436, 1428, 1432, 1414, 1385, 1376, 1443, 1404, 1374, 1376, 1421,
        1418, 1352, 1438, 1419, 1385, 1440, 1390, 1418, 1387, 1355, 1394, 1409,
        1372, 1390, 1409, 1351, 1382, 1386, 1416, 1346, 1421, 1331, 1461, 1463,
        1400, 1380, 1410, 1420, 1385, 1354, 1409, 1335, 1394, 1391, 1414, 1447,
        1354, 1426, 1324, 1431, 1376, 1443, 1349, 1380, 1366, 1405, 1484, 1398,
        1429, 1415, 1364, 1414, 1410, 1392, 1386, 1439, 1425, 1397, 1368, 1431,
        1378, 1395, 1387, 1400, 1318, 1419, 1425, 1399, 1459, 1407, 1400, 1444,
        1460, 1467, 1415, 1400, 1380, 1411, 1468, 1439, 1403, 1422, 1393, 1401,
        1428, 1425, 1443, 1345, 1422, 1390, 1403, 1470, 1351, 1360, 1352, 1421,
        1407, 1452, 1381, 1395, 1400, 1429, 1470, 1445, 1389, 1428, 1402, 1419,
        1437, 1442, 1413, 1433, 1460, 1371, 1396, 1399, 1434, 1446, 1438, 1382,
        1403, 1466, 1385, 1398, 1422, 1361, 1386, 1421, 1331, 1406, 1444, 1360,
        1470, 1402, 1393, 1457, 1345, 1336, 1352, 1414, 1389, 1416, 1362, 1393,
        1393, 1368, 1380, 1369, 1456, 1446, 1427, 1374, 1424, 1455, 1418, 1392],
        [5558, 5240, 5204, 5205, 5250, 5193, 5260, 5146, 5141, 5257, 5215, 5224, 
        5165, 5271, 5210, 5295, 5239, 5242, 5196, 5217, 5122, 5235, 5219, 5226, 
        5177, 5164, 5177, 5200, 5196, 5239, 5198, 5241, 5498, 5582, 5505, 5634, 
        5577, 5516, 5567, 5643, 5566, 5622, 5534, 5669, 5602, 5676, 5637, 5609, 
        5651, 5686, 5699, 5697, 5699, 5689, 5531, 5608, 5670, 5723, 5719, 5633, 
        5588, 5667, 5679, 5691, 5734, 5583, 5647, 5627, 5654, 5670, 5714, 5690, 
        5606, 5632, 5644, 5699, 5544, 5645, 5716, 5728, 5646, 5715, 5661, 5662, 
        5680, 5713, 5684, 5648, 5749, 5697, 5648, 5686, 5656, 5692, 5688, 5596, 
        5646, 5642, 5679, 5672, 5739, 5671, 5620, 5693, 5600, 5738, 5653, 5658, 
        5627, 5632, 5599, 5685, 5651, 5700, 5677, 5772, 5730, 5613, 5660, 5672, 
        5668, 5736, 5726, 5629, 5625, 5646, 5670, 5707, 5722, 5663, 5649, 5681, 
        5724, 5644, 5728, 5715, 5609, 5653, 5663, 5629, 5663, 5634, 5707, 5708, 
        5658, 5700, 5665, 5632, 5647, 5664, 5705, 5689, 5593, 5618, 5635, 5639, 
        5614, 5559, 5592, 5678, 5604, 5659, 5592, 5646, 5749, 5664, 5655, 5734, 
        5616, 5744, 5606, 5719, 5677, 5652, 5630, 5571, 5636, 5700, 5725, 5673, 
        5656, 5598, 5681, 5725, 5676, 5631, 5591, 5644, 5730, 5543, 5619, 5667, 
        5668, 5634, 5713, 5686, 5583, 5698, 5716, 5642, 5568, 5713, 5655, 5654, 
        5702, 5626, 5739, 5675, 5717, 5679, 5655, 5609, 5738, 5755, 5660, 5732, 
        5604, 5694, 5667, 5593, 5680, 5750, 5690, 5670, 5712, 5665, 5756, 5686, 
        5618, 5611, 5695, 5789, 5615, 5631, 5625, 5652, 5697, 5638, 5557, 5662],
        [857, 853, 869, 826, 843, 854, 874, 896, 904, 886, 840, 835, 886, 876,
        896, 801, 873, 863, 845, 861, 888, 879, 866, 891, 864, 887, 872, 894,
        870, 852, 849, 878, 866, 829, 807, 789, 827, 822, 780, 827, 834, 771, 
        836, 834, 790, 785, 783, 804, 838, 778, 770, 793, 797, 757, 861, 844, 
        821, 810, 785, 810, 828, 810, 770, 803, 813, 822, 847, 786, 850, 799, 
        782, 812, 836, 813, 800, 830, 825, 788, 814, 801, 842, 834, 805, 764, 
        755, 798, 797, 801, 782, 801, 799, 796, 840, 844, 819, 827, 795, 828, 
        782, 770, 848, 847, 813, 826, 817, 820, 819, 780, 831, 849, 814, 831, 
        810, 849, 795, 776, 808, 845, 821, 810, 791, 768, 841, 796, 806, 784, 
        832, 779, 826, 797, 785, 791, 824, 784, 787, 796, 809, 841, 819, 833, 
        798, 818, 875, 769, 859, 787, 829, 826, 810, 792, 810, 830, 730, 867, 
        839, 829, 822, 847, 857, 817, 815, 808, 793, 793, 805, 782, 818, 828, 
        839, 755, 819, 835, 800, 832, 798, 826, 823, 795, 803, 805, 808, 819, 
        774, 792, 802, 824, 790, 739, 797, 815, 823, 805, 785, 803, 750, 802, 
        792, 806, 828, 809, 815, 804, 797, 835, 802, 815, 763, 810, 796, 807,
        859, 824, 838, 810, 782, 838, 814, 792, 788, 820, 827, 805, 822, 789, 
        793, 803, 825, 776, 787, 840, 815, 806, 825, 803, 814, 874, 776, 826,
        816, 855]
    ]
    n_predictions = 240
    return classes, n_predictions

# MeasurementFile
def next_unprocessed_measurement_file(family_id):
    q = MeasurementFile.objects.filter(measurement_plan__family__id=family_id)
    q = q.filter(processed=False)
    mf = q.order_by('id').first()
    return mf

def save_measurement_file(location, measurement_plan, processed=False):
    mf = MeasurementFile(location=location, processed=processed, measurement_plan=measurement_plan)
    mf.save()
    return mf

# MeasurementPlan
def get_measurement_plan(pk):
    try:
        mp = MeasurementPlan.objects.get(pk=pk)
        return mp
    except MeasurementPlan.DoesNotExist:
        return None

def get_latest_measurement_plans(n_suggestions=1000):
    measurement_plans = MeasurementPlan.objects.order_by('-date')[:n_suggestions]
    return measurement_plans

def save_measurement_plan_only(n_features, family, based_plan=None):
    measurement_plan = None
    if based_plan != None:
        measurement_plan = MeasurementPlan(n_features=n_features, family=family, 
            based_plan=based_plan)
    else:
        measurement_plan = MeasurementPlan(n_features=n_features, family=family)
    measurement_plan.save()
    return measurement_plan

def save_measurement_plan_complete(n_features, family, classes, metrics, features, based_plan=None):
    measurement_plan = save_measurement_plan_only(n_features, family, based_plan)
    classes_dic = {}
    metrics_dic = {}
    for c in classes:
        measurement_plan_class = save_measurement_plan_class(c['label'], c['name'], measurement_plan)
        print measurement_plan_class.id
        classes_dic[c['label']] = measurement_plan_class
    for m in metrics:
        metric = save_metric(m['name'], measurement_plan, 
            classes_dic[m['class']]
        )
        metrics_dic[m['name']] = metric
    for f in features:
        save_feature(f['index'], f['name'], f['mandatory'], 
            metrics_dic[f['metric']]
        )
    return measurement_plan

def save_measurement_plan_from_json(json_string):
    data = json.loads(json_string)
    family_data = data['family']
    family = save_measurement_plan_family(family_data['name'])
    n_features = data['n_features']
    classes = data['classes']
    metrics = data['metrics']
    features = data['features']
    return save_measurement_plan_complete(n_features, family, classes, metrics, features)

# Predictions
def get_prediction(pk):
    try:
        prediction = Prediction.objects.get(pk=family_id)
        return prediction
    except Prediction.DoesNotExist:
        return None

def get_prediction_data(pk):
   # prediction = get_prediction(pk)
   # if prediction == None:
   #     return None
   # x = []
   # y = []
   # for f in prediction.get_frequencies():
       # name = 'Class ' + f.label
       # x.append(name)
       # y.append(f.frequency)
    x = ['Class 1', 'Class 2', 'Class 3', 'Class 4']
    y = [2091, 1392, 5662, 855]
    data = {
       'x': x,
       'y': y
    }
    return data

def save_prediction(file, svc_model, family):
    p = Prediction(file=file, svc_model=svc_model, family=family)
    p.save()
    return p

# PredictionFrequency
def save_prediction_frequency(label, frequency, prediction):
    pf = PredictionFrequency(label=label, frequency=frequency, prediction=prediction)
    pf.save()
    return pf

###############################################################################

def save_feature(index, name, mandatory, metric):
    f = Feature(index=index, name=name, mandatory=mandatory, metric=metric)
    f.save()
    return f

def save_measurement_plan_class(label, name, measurement_plan):
    mpc = MeasurementPlanClass(label=label, name=name, 
        measurement_plan=measurement_plan
    )
    mpc.save()
    return mpc

def save_metric(name, measurement_plan, measurement_plan_class):
    metric = Metric(name=name, measurement_plan=measurement_plan, 
        measurement_plan_class=measurement_plan_class
    )
    metric.save()
    return metric

# Suggestion methods
def get_latest_suggestions(n_suggestions=100):
    suggestions = Suggestion.objects.order_by('-date')[:n_suggestions]
    return suggestions

def get_feature_selection(pk):
    try:
        feature_selection = FeatureSelection.objects.get(pk=pk)
        return feature_selection
    except FeatureSelection.DoesNotExist:
        return None

def get_latest_classifiers(n_suggestions=1000):
    classifiers = SVCModel.objects.order_by('-id')[:n_suggestions]
    return classifiers

def get_svc_model(pk):
    try:
        svc_model = SVCModel.objects.get(pk=pk)
        return svc_model
    except SVCModel.DoesNotExist:
        return None

def save_class_of_interest(label, name, suggestion):
    coi=ClassOfInterest(label=label, name=name, suggestion=suggestion) 
    coi.save()
    return coi

def save_feature_selection(suggestion, file, n_samples, n_features, selected_features, scores):
    fs = FeatureSelection(file=file, suggestion=suggestion, n_samples=n_samples, n_features=n_features)
    fs.save()
    for x in range(1, n_features+1):
        save_feature_selection_score(x, scores[x-1], fs)
    for i, name in selected_features:
        save_selected_feature(fs, i, name)
    return fs

def save_feature_selection_score(n_features, score, feature_selection):
    fss = FeatureSelectionScore(n_features=n_features, score=score, feature_selection=feature_selection)
    fss.save()
    return fss

def save_selected_feature(feature_selection, index, name):
    sf = SelectedFeature(feature_selection=feature_selection, index=index, name=name)
    sf.save()
    return sf

def save_svc_model(training_file, parameters):
    svc = SVCModel(training_file=training_file, kernel=parameters['kernel'],
        C=parameters['C'], gamma=parameters['gamma'],
        decision_function_shape=parameters['decision_function_shape'],
        cache_size=parameters['cache_size']
    )
    svc.save()
    return svc

def save_model_selection(svc_model, best_score, x_array, y_array, scores):
    model_selection = ModelSelection(best_score=best_score, 
        svc_model=svc_model
    )
    model_selection.save()
    y_len = len(scores)
    for i in range(0, y_len):
        y = y_array[i]
        x_len = len(scores[i])
        for j in range(0,x_len):
            x = x_array[j]
            score = scores[i][j]
            save_grid_search_score(model_selection, x, y, score)
    return model_selection

def save_grid_search_score(model_selection, x, y, score):
    gss = GridSearchScore(x=x, y=y, score=score, 
        model_selection=model_selection
    )
    gss.save()
    return gss

def save_suggestion(classifier, execution_time, measurement_plan):
    s = Suggestion(classifier=classifier, execution_time=execution_time, 
        measurement_plan=measurement_plan
    )
    s.save()
    return s

