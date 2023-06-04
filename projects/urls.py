from django.urls import path
from .views import projects, project, project_sections, project_section, project_images, project_image, snippets, snippet

urlpatterns = [
    path('', projects, name='projects'),
    path('<int:project_id>/', project, name='project'),
    path('<int:project_id>/sections/', project_sections, name='project_sections'),
    path('<int:project_id>/sections/<int:section_id>/', project_section, name='project_section'),
    path('<int:project_id>/images/', project_images, name='project_images'),
    path('<int:project_id>/images/<int:image_id>/', project_image, name='project_image'),
    path('<int:project_id>/code/', snippets, name='snippets'),
    path('<int:project_id>/code/<int:snippet_id>/', snippet, name='snippet'),
]
