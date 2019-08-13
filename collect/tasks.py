from __future__ import absolute_import, unicode_literals
from celery import shared_task

from collect.models import FileUpload


@shared_task
def import_to_db(id):
    obj = FileUpload.objects.get(id=id)
    # todo