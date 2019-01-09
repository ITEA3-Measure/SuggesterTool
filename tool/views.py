# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from suggesterproject.celery import app
from . import suggestermanager
from .filemanager import handle_training_file_upload
from .filemanager import handle_unclassified_file_upload
from .forms import MeasurementPlanForm
from .forms import ModelSelectionForm
from .forms import SuggestionForm
from .modelmanager import get_measurement_plan
from .modelmanager import get_measurement_plan_family_predictions
from .modelmanager import get_latest_classifiers
from .modelmanager import get_latest_measurement_plans
from .modelmanager import get_latest_suggestions
from .modelmanager import get_prediction_data
from .modelmanager import get_svc_model
from .modelmanager import get_feature_selection
from .modelmanager import save_measurement_file
from .modelmanager import save_measurement_plan_from_json
from .tasks import model_selection_task
from .tasks import suggest_task

# modelmanager
from .modelmanager import save_measurement_file

# toolmanager
from .toolmanager import set_current_classifier
from .toolmanager import set_current_measurement_plan

#measureplatformintegration
from .measureplatform import tool_integration
import requests, json

# Create your views here.

def test(request):
    from .logmanager import dummy_export_log
    dummy_export_log('/home/ubuntu/007.log', '/home/ubuntu/007.count.log')
    return HttpResponse('!!!!!!!!!!!!!!')

def test_2(request):
    return HttpResponse('!!!!!!!!!!!!!!')

def test_3(request):
    return HttpResponse('!!!!!!!!!!!!!!')

def index(request):
    template = loader.get_template('tool/index.html')
    context = {
        'nbar': 'home'
    }
    tool_integration()
    return HttpResponse(template.render(context, request))

def completed_task(request):
    template = loader.get_template('tool/task_success.html')
    context = {
        'nbar': ''
    }
    return HttpResponse(template.render(context, request))

def classifiers(request):
    row_titles = ['ID', 'Kernel', 'CV Score']
    template_classifiers = []
    for classifier in get_latest_classifiers():
        dictionary = {
            'svc_id': classifier.id,
            'kernel': classifier.kernel,
            'cv_score': classifier.get_model_selection_score()
        }
        template_classifiers.append(dictionary)
    template = loader.get_template('tool/classifiers.html')
    context = {
        'nbar': 'classifier',
        'row_titles': row_titles,
        'classifiers': template_classifiers
    }
    return HttpResponse(template.render(context, request))

def classifier_view(request, pk):
    template = loader.get_template('tool/classifier.html')
    context = {
        'nbar': 'classifier_view',
        'primary_key': pk
    }
    return HttpResponse(template.render(context, request))

def dashboard_view(request):
    template = loader.get_template('tool/dashboard.html')
    context = {
        'nbar': 'plan_view',
        'family_key': 1,
        'latest_prediction_key': 1,
        'current_classifier': 1,
        'current_plan': 1, 
    }
    return HttpResponse(template.render(context, request))

def prediction_view(request, pk):
    template = loader.get_template('tool/prediction.html')
    context = {
        'nbar': 'plan_view',
        'primary_key': pk
    }
    return HttpResponse(template.render(context, request))

def predictions_view(request, pk):
    template = loader.get_template('tool/family_predictions.html')
    context = {
        'nbar': 'plan_view',
        'primary_key': pk
    }
    return HttpResponse(template.render(context, request))

def feature_selection_view(request, pk):
    template = loader.get_template('tool/feature_selection.html')
    context = {
        'nbar': 'feature_selection_view',
        'primary_key': pk
    }
    return HttpResponse(template.render(context, request))

def measurement_plan_view(request, pk):
    mp = get_measurement_plan(pk)
    classes = []
    for mpc in mp.get_classes():
        dic = {
            'label': mpc.label,
            'name': mpc.name
        }
        classes.append(dic)
    metrics = []
    for m in mp.get_metrics():
        dic = {
            'class': m.measurement_plan_class.label,
            'name': m.name,
            'features': ','.join(m.get_features_names()),
            'mandatory': ','.join(m.get_mandatory_features_names())
        }
        metrics.append(dic)
    template = loader.get_template('tool/plan.html')
    context = {
        'nbar': 'plan_view',
        'n_features': mp.n_features,
        'plan_id': mp.id,
        'classes': classes,
        'metrics': metrics
    }
    return HttpResponse(template.render(context, request))

def measurement_plans(request):
    row_titles = ['ID', 'No. Features', 'Classes', 'Metrics']
    template_plans = []
    for mp in get_latest_measurement_plans():
        dictionary = {
            'plan_id': mp.id,
            'n_features': mp.n_features,
            'classes': ','.join(mp.get_classes_names()),
            'metrics': ','.join(mp.get_metrics_names())
        }
        template_plans.append(dictionary)
    template = loader.get_template('tool/plans.html')
    context = {
        'nbar': 'plans',
        'row_titles': row_titles,
        'plans': template_plans
    }
    return HttpResponse(template.render(context, request))

def model_selection_form(request):
    if request.method == 'POST':
        form = ModelSelectionForm(request.POST, request.FILES)
        if form.is_valid():
            file = handle_training_file_upload(request.FILES['training_file'])
            result = model_selection_task.delay(file)
            return redirect('wait_task_view', result.id)
    else:
        form = ModelSelectionForm()
    return render(request, 'tool/model_selection_form.html', {'form': form})

def post_measurement_plan(request):
    if request.method == 'POST':
        form = MeasurementPlanForm(request.POST)
        if form.is_valid():
            json_string = form.cleaned_data['measurement_plan_json']
            save_measurement_plan_from_json(json_string)
            return redirect('tool_index')
    else:
        form = MeasurementPlanForm()
    return render(request, 'tool/measurement_plan_form.html', {'form': form})

def suggestions(request):
    row_titles = ['Classes of Interest', 'No. Instances', 'Classifier ID', 'MP Features', 'Execution Time']
    template_suggestions = []
    for suggestion in get_latest_suggestions():
        dictionary = {
            'classes_of_interest': suggestion.get_classes_of_interest_str(),
            'n_instances': suggestion.get_number_of_instances(),
            'classifier_id': suggestion.classifier.id,
            'removed_features': suggestion.get_removed_features_str(),
            'execution_time': suggestion.execution_time
        }
        template_suggestions.append(dictionary)
    template = loader.get_template('tool/suggestions.html')
    context = {
        'nbar': 'suggestions',
        'row_titles': row_titles,
        'suggestions': template_suggestions
    }
    return HttpResponse(template.render(context, request))

def suggestion_form(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            file = handle_unclassified_file_upload(request.FILES['unclassified_file'])
            mp = form.cleaned_data['measurement_plan']
            model = form.cleaned_data['model']
            set_current_classifier(model)
            set_current_measurement_plan(mp)
            save_measurement_file(file, mp)
            result = suggest_task.delay()
            return redirect('wait_task_view', result.id)
            # return redirect('tool_index')
    else:
        form = SuggestionForm()
    return render(request, 'tool/upload_file.html', {'form': form})

def wait_task(request, task_id):
    template = loader.get_template('tool/wait_task.html')
    context = {
        'nbar': '',
        'task_id': task_id
    }
    return HttpResponse(template.render(context, request))

@api_view(['GET'])
def feature_selection_score_data(request, pk):
    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    feature_selection = get_feature_selection(pk)
    if feature_selection == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    x = []
    y = []
    for fss in feature_selection.featureselectionscore_set.order_by('n_features'):
        x.append(fss.n_features)
        y.append(fss.score)
    data = {
        'x': x,
        'y': y
    }
    return Response(data)

@api_view(['GET'])
def measurement_plan_family_predictions(request, pk):
    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    predictions, n_predictions = get_measurement_plan_family_predictions(pk)
    if predictions == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {
        'n_predictions': n_predictions,
        'predictions': predictions
    }
    print data
    return Response(data)

@api_view(['GET'])
def prediction_data(request, pk):
    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    data = get_prediction_data(pk)
    if data == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(data)    

@api_view(['GET'])
def svc_model_selection_heatmap_data(request, pk):
    """
    Retrieve heatmap data from model selection of a classifier.
    """
    if request.method != 'GET':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    svc_model = get_svc_model(pk)
    if svc_model == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = {
        'x': [],
        'y': [],
        'z': []
    }
    model_selection = svc_model.modelselection
    if model_selection != None:
        x_set = set()
        y_set = set()
        heatmap = {}
        for gss in model_selection.gridsearchscore_set.all():
            x = gss.x
            y = gss.y
            score = gss.score
            map_key = (x, y)
            x_set.add(x)
            y_set.add(y)
            heatmap[map_key] = score
        x_array = sorted(list(x_set))
        y_array = sorted(list(y_set))
        z_array = []
        for y in y_array:
            row = []
            for x in x_array:
                map_key = (x, y)
                row.append(heatmap[map_key])
            z_array.append(row)
        data['x'] = x_array
        data['y'] = y_array
        data['z'] = z_array
    return Response(data)

@api_view(['GET'])
def task_state(request, task_id):
    task = app.AsyncResult(task_id)
    state = task.state
    data = {'state': state}
    if state == 'SUCCESS':
        data['redirect'] = reverse('completed_task_view')
    return Response(data)

class UploadFile(APIView):
    parser_classes = (MultiPartParser, FormParser,)

class UploadUnclassifiedFile(UploadFile):
    
    def post(self, request, format=None):
        upload = request.FILES['file']
        file = handle_unclassified_file_upload(upload)
        suggestermanager.add_file_to_prediction_list(file, [])
        return Response({}, status=201)
