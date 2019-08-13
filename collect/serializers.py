
from rest_framework import serializers

from collect.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'file')
        model = FileUpload