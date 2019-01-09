# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.

class MeasurementPlanFamily(models.Model):
    name = models.CharField(max_length=200)

    def get_predictions(self):
        predictions = []
        for p in self.prediction_set.order_by('date'):
            predictions.append(p)
        return predictions

    def get_first_measurement_plan(self):
        mp = self.measurementplan_set.order_by('date').first()
        return mp

class MeasurementFile(models.Model):
    location = models.CharField(max_length=500)
    processed = models.BooleanField(default=False)
    measurement_plan = models.ForeignKey(
        'MeasurementPlan', 
        on_delete=models.CASCADE
    )

class Feature(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=200)
    mandatory = models.BooleanField()
    metric = models.ForeignKey(
        'Metric', 
        on_delete=models.CASCADE
    )

class MeasurementPlan(models.Model):
    n_features = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(
        'MeasurementPlanFamily', 
        on_delete=models.CASCADE
    )
    based_plan = models.OneToOneField(
        'self', blank=True, null=True
    )

    def get_features(self):
        features = []
        for m in self.get_metrics():
            features.extend(m.get_features())
        features = sorted(features, key=lambda f: f.index)
        return features

    def get_features_names(self):
        names = []
        for f in self.get_features():
            names.append(f.name)
        return names

    def get_mandatory_features(self):
        mandatory = []
        for f in self.get_features():
            if f.mandatory:
                mandatory.append(f)
        return mandatory

    def get_mandatory_features_names(self):
        names = []
        for f in self.get_mandatory_features():
            names.append(f.name)
        return names

    def get_classes(self):
        classes = []
        for mpc in self.measurementplanclass_set.order_by('label'):
            classes.append(mpc)
        return classes

    def get_classes_names(self):
        names = []
        for mpc in self.get_classes():
            names.append(mpc.name)
        return names

    def get_metrics(self):
        metrics = []
        for m in self.metric_set.all():
            metrics.append(m)
        return metrics

    def get_metrics_names(self):
        names = []
        for m in self.get_metrics():
            names.append(m.name)
        return names

class MeasurementPlanClass(models.Model):
    label = models.IntegerField()
    name = models.CharField(max_length=200)
    measurement_plan = models.ForeignKey(
        'MeasurementPlan', 
        on_delete=models.CASCADE
    )

class Metric(models.Model):
    name = models.CharField(max_length=200)
    measurement_plan_class = models.ForeignKey(
        'MeasurementPlanClass', 
        on_delete=models.CASCADE
    )
    measurement_plan = models.ForeignKey(
        'MeasurementPlan', 
        on_delete=models.CASCADE
    )

    def get_features(self):
        features = []
        for f in self.feature_set.order_by('index'):
            features.append(f)
        return features

    def get_features_names(self):
        names = []
        for f in self.get_features():
            names.append(f.name)
        return names

    def get_mandatory_features(self):
        mandatory = []
        for f in self.get_features():
            if f.mandatory:
                mandatory.append(f)
        return mandatory

    def get_mandatory_features_names(self):
        names = []
        for f in self.get_mandatory_features():
            names.append(f.name)
        return names

class Prediction(models.Model):
    file = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    svc_model = models.ForeignKey(
        'SVCModel', 
        on_delete=models.CASCADE
    )
    family = models.ForeignKey(
        'MeasurementPlanFamily', 
        on_delete=models.CASCADE
    )

    def get_frequencies(self):
        frequencies = list(self.predictionfrequency_set.order_by('label'))
        return frequencies

class PredictionFrequency(models.Model):
    label = models.IntegerField()
    frequency = models.IntegerField()
    prediction = models.ForeignKey(
        'Prediction', 
        on_delete=models.CASCADE
    )

class SVCModel(models.Model):
    training_file = models.CharField(max_length=200)
    kernel = models.CharField(max_length=200)
    C = models.FloatField(default=0.0)
    gamma = models.FloatField(default=0.0)
    decision_function_shape = models.CharField(max_length=200)
    cache_size = models.FloatField(default=0.0)

    def get_model_selection_score(self):
        model_selection = self.modelselection
        if model_selection != None:
            return model_selection.best_score
        else:
            return 0

class ModelSelection(models.Model):
    best_score = models.FloatField(default=0.0)
    svc_model = models.OneToOneField(
        'SVCModel',
        on_delete=models.CASCADE,
        primary_key=True,
    )

class GridSearchScore(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    score = models.FloatField(default=0.0)
    model_selection = models.ForeignKey(
        ModelSelection, 
        on_delete=models.CASCADE
    )

class Suggestion(models.Model):
    # {'id': 1, 'classes_of_interest': '3', 'predicted_instances': 10000, 'classifier_id': 1, 'removed_features': "Code Size, No. Bugs", 'execution_time': 5.1435}
    classifier = models.ForeignKey(
        'SVCModel', 
        on_delete=models.CASCADE
    )
    measurement_plan = models.ForeignKey(
        'MeasurementPlan', 
        on_delete=models.CASCADE
    )
    suggested_measurement_plan_id = models.IntegerField(default=-1)
    date = models.DateTimeField(auto_now_add=True)
    execution_time = models.FloatField(default=0.0)
    def get_classes_of_interest_str(self):
        classes_of_interest = []
        for class_of_interest in self.classofinterest_set.all():
            classes_of_interest.append(class_of_interest.name)
        return ','.join(classes_of_interest)

    def get_number_of_instances(self):
        try:
            return self.featureselection.n_samples
        except ObjectDoesNotExist:
            return 0 

    def get_removed_features_str(self):
        try:
            removed_features = []
            for feature in self.featureselection.selectedfeature_set.all():
                removed_features.append(feature.name)
            return ','.join(removed_features)
        except ObjectDoesNotExist:
            return ''

    class Meta:
        ordering = ['-date']

class ClassOfInterest(models.Model):
    label = models.IntegerField()
    name = models.CharField(max_length=200)
    suggestion = models.ForeignKey(
        Suggestion, 
        on_delete=models.CASCADE
    )

class FeatureSelection(models.Model):
    file = models.CharField(max_length=200)
    suggestion = models.OneToOneField(
        Suggestion,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    n_samples = models.IntegerField()
    n_features = models.IntegerField()

    def get_selected_features(self):
        features = []
        for sf in self.selectedfeature_set.order_by('index'):
            features.append(sf)
        return features

    def get_selected_features_names(self):
        names = []
        for sf in self.get_selected_features():
            names.append(sf.name)
        return names

class FeatureSelectionScore(models.Model):
    n_features = models.IntegerField()
    score = models.FloatField(default=0.0)
    feature_selection = models.ForeignKey(
        FeatureSelection, 
        on_delete=models.CASCADE
    )

class SelectedFeature(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=200)
    feature_selection = models.ForeignKey(
        FeatureSelection, 
        on_delete=models.CASCADE
    )
