from django.urls import path
from . import views

urlpatterns = [
    path('', views.categories_view, name='blog_categories'),
    path('recent/', views.recent_posts, name="recent_posts"),
    path('<str:category>/', views.category_view, name='blog_category'),
    path('<str:category>/posts/', views.posts_view, name='blog_posts'),
    path('<str:category>/posts/<slug:slug>/', views.post_view, name='blog_post'),
    path('<str:category>/posts/<slug:slug>/related/', views.related_view, name='blog_related'),
    path('<str:category>/posts/<slug:slug>/related/<int:id>/', views.change_related_view, name='blog_change_related'),
    path('<str:category>/posts/<slug:slug>/<str:type>/', views.contents_view, name='blog_contents'),
    path('<str:category>/posts/<slug:slug>/<str:type>/<int:id>/', views.content_view, name='blog_content'),
]