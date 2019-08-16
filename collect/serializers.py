from rest_framework import serializers

from collect.models import FileUpload, Data, TeamFileUpload, Team


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "file")
        model = FileUpload


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ("data", "order_placed")


class TeamFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "file")
        model = TeamFileUpload


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("team_name", "manager_name", "manager_phone_number")
        model = Team
