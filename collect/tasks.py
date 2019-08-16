from __future__ import absolute_import, unicode_literals

import datetime
import time

import celery
import pytz
from celery import shared_task, states
from django.conf import settings
from django.utils.timezone import make_aware
from django_celery_results.models import TaskResult

from collect.models import FileUpload, Data, TeamFileUpload, Team

import pandas as pd


DATETIME_FORMAT = "%m/%d/%Y"

# TODO: Set Retry
@shared_task(bind=True)
def import_to_db(self, id):
    print("In import_to_db")
    obj = FileUpload.objects.get(id=id)
    print("here in import_to_db")

    # Download the file and import into db
    url = obj.file.url

    df = pd.read_csv(url)
    print("Downloaded the file")

    for index, data in df.iterrows():
        data_dict = data.to_dict()
        print("data_dict", data_dict)

        order_placed = datetime.datetime.strptime(
            data_dict["Order Date"], DATETIME_FORMAT
        )
        # timezone.activate(pytz.timezone(settings.TIME_ZONE))
        timezone_aware_time = make_aware(
            order_placed, timezone=pytz.timezone(settings.TIME_ZONE)
        )
        print("order placed", order_placed)
        try:
            data_obj = Data.objects.create(
                file_upload=obj, data=data_dict, order_placed=timezone_aware_time
            )
        except Exception as e:
            print("Some error occured", e)


# Todo: set retry
@shared_task(bind=True)
def create_teams(self, id):
    print("In create_teams")
    obj = TeamFileUpload.objects.get(id=id)
    print("here in create_teams")

    # Download the file and import into db
    url = obj.file.url

    df = pd.read_csv(url)
    print("Downloaded the file")

    for index, data in df.iterrows():
        data_dict = data.to_dict()
        data_dict = {key.strip(): val.strip() for key, val in data_dict.items()}
        print("data_dict", data_dict)
        data_dict["file_upload"] = obj

        try:
            data_obj = Team.objects.create(**data_dict)
            # Just to extend the process of team creation
            time.sleep(2)
        except Exception as e:
            print("Some error occured", e)


@shared_task(bind=True)
def delete_teams(self, id):
    obj = TeamFileUpload.objects.get(id)
    task = TaskResult.objects.get(task_id=obj.task_id)
    if task.status in [states.RECEIVED, states.STARTED, states.PENDING, states.RETRY]:
        print("Revoking the task")
        celery.task.control.revoke(obj.task_id)
    obj.delete()
