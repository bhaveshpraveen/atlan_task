from rest_framework import permissions

from collect.models import FileUpload
from django_celery_results.models import TaskResult

from celery import states


class IsAllowedToUpload(permissions.BasePermission):
    UNALLOWED_STATES = [states.RECEIVED, states.STARTED, states.PENDING, states.RETRY]
    file_upload_queryset = FileUpload.objects.all()

    def has_permission(self, request, view):
        user = self.request.user
        uploads = self.file_upload_queryset.filter(user=user)

        for upload in uploads:
            task = TaskResult.objects.get(task_id=upload.task_id)
            if task.status in IsAllowedToUpload.UNALLOWED_STATES:
                return False
        return True


class IsTaskOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class IsPatch(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "PATCH"


class IsPut(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "PUT"


class IsGet(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "GET"


class IsDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "DELETE"