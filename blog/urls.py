from django.urls import path
from . import views

urlpatterns = [
    path('', views.categories_view, name='blog_categories'),
    path('<str:category>/', views.posts_view, name='blog_posts'),
    path('<str:category>/<slug:slug>/', views.content_view, name='blog_contents'),
]