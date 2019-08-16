import datetime

import celery
import django_celery_results
import pytz
from celery import states
from django.utils.timezone import make_aware
from django_celery_results.models import TaskResult

from rest_framework import generics, status
from rest_framework import permissions
from rest_condition import Or, And
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from atlan_task import settings
from collect import serializers
from collect.models import FileUpload, Data, TeamFileUpload
from collect.pagination import DataLimitOffsetPagination, FileUploadLimitOffsetPagination, TeamFileLimitOffsetPagination
from collect.permissions import IsAllowedToUpload, IsTaskOwner, IsGet, IsDelete, IsPost
from collect.tasks import import_to_db, create_teams, delete_teams


class BaseLineUpload(generics.ListCreateAPIView):
    serializer_class = serializers.FileUploadSerializer
    queryset = FileUpload.objects.all()
    pagination_class = FileUploadLimitOffsetPagination
    # TODO: UPDATE PERMISSIONS
    permission_classes = [
        Or(
            And(
                IsGet,
                permissions.IsAuthenticated
            ),
            And(
                IsPost,
                permissions.IsAuthenticated,
                IsAllowedToUpload
            ),
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
    queryset = Data.objects.all().select_related("file_upload")
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = DataLimitOffsetPagination
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


class TeamFileUploadListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.TeamFileUploadSerializer
    queryset = TeamFileUpload.objects.all()
    pagination_class = TeamFileLimitOffsetPagination
    # TODO: UPDATE PERMISSIONS
    permission_classes = [
        And(
            Or(IsGet, IsPost),
            permissions.IsAuthenticated
        ),

    ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        task = create_teams.delay(obj.id)
        # Set the task id
        obj.task_id = task.task_id
        obj.save()


class TeamFileUploadDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TeamFileUploadSerializer
    task_result_queryset = TaskResult.objects.all()
    queryset = TeamFileUpload.objects.all()
    permission_classes = [
        And(
            Or(IsGet, IsDelete),
            permissions.IsAuthenticated,
            IsTaskOwner
        )
    ]

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        # delete_teams.delay(obj.id)
        task = self.task_result_queryset.get(task_id=obj.task_id)
        if task.status in [states.RECEIVED, states.STARTED, states.PENDING, states.RETRY]:
            print('Revoking the task')
            celery.task.control.revoke(obj.task_id, terminate=True)
        # Else: Its already completed
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






