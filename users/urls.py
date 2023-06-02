from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('check/', views.check_session, name='check'),
    path('logout/', views.logout_view, name="logout"),
]