from django.urls import path
from . import views


urlpatterns = [
    path('', views.messages, name='messages'),
    path('send/', views.send, name='send'),
]