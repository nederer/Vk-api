from django.urls import path
from TestApp import views


urlpatterns = [
    path('main/', views.main_page),
    path('register/', views.register),
]