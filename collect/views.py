from django.shortcuts import render

from rest_framework import generics

from collect import serializers
from collect.models import FileUpload
from collect.tasks import import_to_db


class BaseLineUpload(generics.CreateAPIView):
    serializer_class = serializers.FileUploadSerializer
    queryset = FileUpload.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save()
        task = import_to_db.delay(obj.id)
        obj.task_id = task.task_id
        # task = import_to_db(obj.id)