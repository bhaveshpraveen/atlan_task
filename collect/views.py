import datetime

import pytz
from django.utils.timezone import make_aware

from rest_framework import generics
from rest_framework import permissions
from rest_condition import Or, And

from atlan_task import settings
from collect import serializers
from collect.models import FileUpload, Data
from collect.permissions import IsAllowedToUpload, IsTaskOwner, IsGet, IsDelete
from collect.tasks import import_to_db


class BaseLineUpload(generics.ListCreateAPIView):
    serializer_class = serializers.FileUploadSerializer
    queryset = FileUpload.objects.all()
    # TODO: UPDATE PERMISSIONS
    permission_classes = [
        And(
            permissions.IsAuthenticated,
            IsAllowedToUpload
        )
    ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        task = import_to_db.delay(obj.id)
        # Set the task id
        obj.task_id = task.task_id
        obj.save()


class BaseLineUploadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FileUploadSerializer
    queryset = FileUpload.objects.all()
    permission_classes = [
        And(
            Or(IsGet, IsDelete),
            permissions.IsAuthenticated,
            IsAllowedToUpload,
            IsTaskOwner
        )
    ]


class DataListView(generics.ListAPIView):
    serializer_class = serializers.DataSerializer
    queryset = Data.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    QUERY_DATE_FORMAT = '%Y-%m-%d'

    def filter_by_date(self, qs):
        date_str = self.request.query_params.get('from')
        if date_str:
            date = datetime.datetime.strptime(date_str, DataListView.QUERY_DATE_FORMAT)
            timezone_aware_date = make_aware(date, timezone=pytz.timezone(settings.TIME_ZONE))
            return qs.filter(order_placed__gte=timezone_aware_date)
        return qs

    def get_queryset(self):
        qs = self.queryset.filter(file_upload__user=self.request.user)
        return self.filter_by_date(qs)


class TeamCreateView(generics.CreateAPIView):
    permission_classes = [

    ]

    def post(self, request, *args, **kwargs):
        # Task that creates 1000 teams.
        pass


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    def delete(self, request, *args, **kwargs):
        pass
        






