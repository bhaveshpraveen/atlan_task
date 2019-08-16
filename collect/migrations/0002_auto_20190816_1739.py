# Generated by Django 2.2.4 on 2019-08-16 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("collect", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(name="data", options={"ordering": ("-id",)}),
        migrations.AlterModelOptions(name="fileupload", options={"ordering": ("-id",)}),
        migrations.CreateModel(
            name="TeamFileUpload",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "task_id",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="celery_task_id"
                    ),
                ),
                ("file", models.FileField(upload_to="")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_file_uploads",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("-id",)},
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "team_name",
                    models.CharField(max_length=100, verbose_name="Team name"),
                ),
                (
                    "manager_name",
                    models.CharField(max_length=100, verbose_name="Manager name"),
                ),
                (
                    "manager_phone_number",
                    models.CharField(max_length=15, verbose_name="Phone number"),
                ),
                (
                    "file_upload",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams",
                        to="collect.TeamFileUpload",
                    ),
                ),
            ],
            options={"ordering": ("-id",)},
        ),
    ]
