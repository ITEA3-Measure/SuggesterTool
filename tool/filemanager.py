# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import expanduser
from os.path import join
import uuid

USER_PATH = expanduser('~')
PROJECT_PATH = join(USER_PATH, 'suggester_tool/')
CLASSIFIED_DATA_DIRECTORY = join(PROJECT_PATH, 'classified_data')
PREDICTED_DATA_DIRECTORY = join(PROJECT_PATH, 'predicted_data')
UNCLASSIFIED_DATA_DIRECTORY = join(PROJECT_PATH, 'unclassified_data')

def _unique_filename():
    unique_filename = str(uuid.uuid4())
    return unique_filename

def get_new_filename_for_predicted_data():
    filename = _unique_filename() + '.p'
    path = join(PREDICTED_DATA_DIRECTORY, filename)
    return path

def get_new_filename_for_classified_data():
    filename = _unique_filename() + '.tr'
    path = join(CLASSIFIED_DATA_DIRECTORY, filename)
    return path

def handle_file_upload(path, file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path

def handle_training_file_upload(file):
    filename = _unique_filename() + '.tr'
    path = join(CLASSIFIED_DATA_DIRECTORY, filename)
    return handle_file_upload(path, file)

def handle_unclassified_file_upload(file):
    filename = _unique_filename() + '.un'
    path = join(UNCLASSIFIED_DATA_DIRECTORY, filename)
    return handle_file_upload(path, file)
