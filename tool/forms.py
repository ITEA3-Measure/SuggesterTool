# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import MeasurementPlan
from .models import SVCModel

# Create your forms here.

class MeasurementPlanForm(forms.Form):
    measurement_plan_json = forms.CharField(widget=forms.Textarea)

class ModelSelectionForm(forms.Form):
    training_file = forms.FileField()

class SuggestionForm(forms.Form):
    measurement_plan = forms.ModelChoiceField(queryset=MeasurementPlan.objects.all())
    model = forms.ModelChoiceField(queryset=SVCModel.objects.all())
    unclassified_file = forms.FileField()
