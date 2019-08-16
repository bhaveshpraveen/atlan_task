from django.contrib.postgres.fields import JSONField
from django.db import models

from django.contrib.auth import get_user_model


class FileUpload(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='file_uploads')
    task_id = models.CharField(verbose_name='celery_task_id', max_length=150, blank=True)
    file = models.FileField()

    def __str__(self):
        return f'id: {self.id}, task_id: {self.task_id}'


class Data(models.Model):
    file_upload = models.ForeignKey('FileUpload', related_name='data', on_delete=models.CASCADE)
    data = JSONField()
    order_placed = models.DateTimeField(verbose_name='Order Placed')

    def __str__(self):
        return f'pk = {self.pk}, data={self.data}'


class TeamFileUpload(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='file_uploads')
    task_id = models.CharField(verbose_name='celery_task_id', max_length=150, blank=True)
    file = models.FileField()


class Team(models.Model):
    team_id = models.PositiveIntegerField(primary_key=True)
    players = JSONField()
    manager = JSONField()


# class Team(models.Model):
#     team_id = models.PositiveIntegerField(primary_key=True)
#     player = models.ForeignKey('Player', related_name='team', on_delete=models.CASCADE)
#     manager = models.ForeignKey('Manager', related_name='manager', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.team_id}'
#
#
# class Player(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.PositiveIntegerField()
#     player_gender = models.CharField(max_length=1)
#
#     def __str__(self):
#         return f'name: {self.name}, age: {self.age}'

