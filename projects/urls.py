from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:project_id>/sections/', views.project_sections, name='project_sections'),
    path('<int:project_id>/sections/<int:section_id>/', views.project_section, name='project_section'),
    path('<int:project_id>/images/', views.project_images, name='project_images'),
    path('<int:project_id>/images/<int:image_id>/', views.project_image, name='project_image'),
    path('<int:project_id>/videos/', views.project_videos, name='project_videos'),
    path('<int:project_id>/videos/<int:video_id>/', views.project_video, name='project_video'),
    path('<int:project_id>/code/', views.snippets, name='snippets'),
    path('<int:project_id>/code/<int:snippet_id>/', views.snippet, name='snippet'),
    path('<int:project_id>/tech/', views.tech_view, name='tech')
]
