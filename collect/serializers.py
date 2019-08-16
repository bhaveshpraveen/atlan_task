
from rest_framework import serializers

from collect.models import FileUpload, Data


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'file')
        model = FileUpload


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('data', 'order_placed')