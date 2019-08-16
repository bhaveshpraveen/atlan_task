from django.urls import path

from collect import views

urlpatterns = [
    # Example 1
    path('baseline/', views.BaseLineUpload.as_view()),
    path('baseline/<int:pk>/', views.BaseLineUploadDetailView.as_view()),


    path('data/', views.DataListView.as_view()),

    # Example 3
    path('team/', views.TeamFileUploadListCreateView.as_view()),
    path('team/<int:pk>/', views.TeamFileUploadDetailView.as_view())

]