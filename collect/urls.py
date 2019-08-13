from django.urls import path

from collect import views

urlpatterns = [
    path('upload/', views.BaseLineUpload.as_view()),
]