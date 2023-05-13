from django.urls import path
from .views import projects, project, project_sections, project_section, project_images, project_image, apps, app, app_sections, app_section, app_images, app_image, snippets, snippet

urlpatterns = [
    path('', projects, name='projects'),
    path('<int:project_id>/', project, name='project'),
    path('<int:project_id>/sections/', project_sections, name='project_sections'),
    path('<int:project_id>/sections/<int:section_id>/', project_section, name='project_section'),
    path('<int:project_id>/images/', project_images, name='project_images'),
    path('<int:project_id>/images/<int:image_id>/', project_image, name='project_image'),
    path('<int:project_id>/apps/', apps, name='apps'),
    path('<int:project_id>/apps/<int:app_id>/', app, name='app'),
    path('<int:project_id>/apps/<int:app_id>/sections/', app_sections, name='app_sections'),
    path('<int:project_id>/apps/<int:app_id>/sections/<int:section_id>/', app_section, name='app_section'),
    path('<int:project_id>/apps/<int:app_id>/images/', app_images, name='app_images'),
    path('<int:project_id>/apps/<int:app_id>/images/<int:image_id>/', app_image, name='app_image'),
    path('<int:project_id>/code/', snippets, name='snippets'),
    path('<int:project_id>/code/<int:snippet_id>/', snippet, name='snippet'),
]
