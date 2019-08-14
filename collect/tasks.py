from __future__ import absolute_import, unicode_literals

import datetime
import random
import string
import time

import pytz
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_aware

from collect.models import FileUpload, Data

import pandas as pd


DATETIME_FORMAT = '%m/%d/%Y'

#TODO: Set Retry
@shared_task(bind=True)
def import_to_db(self, id):
    print('In import_to_db')
    obj = FileUpload.objects.get(id=id)
    print('here in import_to_db')
    # set the task_id
    obj.task_id = self.request.id
    # obj.task_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    obj.save()

    # Download the file and import into db
    url = obj.file.url

    df = pd.read_csv(url)
    print('Downloaded the file')


    for index, data in df.iterrows():
        data_dict = data.to_dict()
        print('data_dict', data_dict)

        order_placed = datetime.datetime.strptime(data_dict['Order Date'], DATETIME_FORMAT)
        # timezone.activate(pytz.timezone(settings.TIME_ZONE))
        timezone_aware_time = make_aware(order_placed, timezone=pytz.timezone(settings.TIME_ZONE))
        print('order placed', order_placed)
        try:
            data_obj = Data.objects.create(file_upload=obj, data=data_dict, order_placed=timezone_aware_time)

        except Exception as e:
            print('Some error occured', e)

    print('Going to sleep')
    time.sleep(60)
    print('Came outta sleep')





