# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

# Add urls to your views here.

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^test2/$', views.test_2, name='test2'),
    url(r'^test3/$', views.test_3, name='test3'),
    url(r'^$', views.index, name='tool_index'),
    url(r'^api/files/unclassified/$', views.UploadUnclassifiedFile.as_view(), name='api_unclassified_file'),
    url(r'^api/svcmodels/(?P<pk>[0-9]+)/data/heatmap/$', views.svc_model_selection_heatmap_data, name='api_svc_heatmap_data'),
    url(r'^api/featureselection/(?P<pk>[0-9]+)/data/scores/$', views.feature_selection_score_data, name='api_feature_selection_scores'),
    url(r'^api/plan/family/(?P<pk>[0-9]+)/predictions/$', views.measurement_plan_family_predictions, name='api_measurement_plan_family_predictions'),
    url(r'^api/prediction/(?P<pk>[0-9]+)/$', views.prediction_data, name='api_prediction_data'),
    url(r'^api/tasks/(?P<task_id>[-\w]+)/state/$', views.task_state, name='api_task_state'),
    url(r'^view/classifiers/$', views.classifiers, name='classifiers_all'),
    url(r'^view/classifiers/(?P<pk>[0-9]+)/$', views.classifier_view, name='classifier_view'),
    url(r'^view/dashboard/$', views.dashboard_view, name='dashboard_view'),
    url(r'^view/featureselection/(?P<pk>[0-9]+)/$', views.feature_selection_view, name='feature_selection_view'),
    url(r'^view/modelselection/form/$', views.model_selection_form, name='model_selection_form'),
    url(r'^view/plans/$', views.measurement_plans, name='plans_all'),
    url(r'^view/plans/families/(?P<pk>[0-9]+)/predictions/$', views.predictions_view, name='predictions_view'),
    url(r'^view/plans/(?P<pk>[0-9]+)/$', views.measurement_plan_view, name='plan_view'),
    url(r'^view/plans/form/$', views.post_measurement_plan, name='post_measurement_plan'),
    url(r'^view/prediction/(?P<pk>[0-9]+)/$', views.prediction_view, name='prediction_view'),
    url(r'^view/suggestions/$', views.suggestions, name='suggestions_all'),
    url(r'^view/suggestions/form/$', views.suggestion_form, name='suggestion_form'),
    url(r'^view/tasks/(?P<task_id>[-\w]+)/wait/$', views.wait_task, name='wait_task_view'),
    url(r'^view/tasks/success/$', views.completed_task, name='completed_task_view'),
]
