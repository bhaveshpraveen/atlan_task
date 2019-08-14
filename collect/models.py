from django.contrib.postgres.fields import JSONField
from django.db import models


class FileUpload(models.Model):
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
