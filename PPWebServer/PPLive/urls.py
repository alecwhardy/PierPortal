from django.urls import path

from . import views

urlpatterns = [
    path('', views.LiveView.as_view(), name='index'),
]