from django.urls import path
from .views import projects, project, apps, app, project_images, project_image

urlpatterns = [
    path('', projects, name='projects'),
    path('<str:project_name>/', project, name='project'),
    path('<str:project_name>/apps/', apps, name='apps'),
    path('<str:project_name>/apps/<str:app_name>/', app, name='app'),
    path('<str:project_name>/images/', project_images, name='project_images'),
    path('<str:project_name>/images/<int:image_id>/', project_image, name='project_image'),
]
