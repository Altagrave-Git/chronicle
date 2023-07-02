from django.urls import path
from . import views


urlpatterns = [
    path('', views.messages, name='messages'),
    path('<int:id>/', views.message, name="message"),
    path('send/', views.send, name='send'),
    path('check/', views.check, name="check_messages")
]