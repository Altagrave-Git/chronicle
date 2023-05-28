from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.sessions.models import Session


@api_view(['GET'])
def chronicle(request):
    data = [
        'Hello, welcome to chronicle API',
        {
            'auth': False
        },
        {
        'endpoints': {
            'projects': '/projects/',
            'project': '/projects/:id/',
            'project_sections': '/projects/:id/sections/',
            'project_section': '/projects/:id/sections/:id/',
            'project_images': '/projects/:id/images/',
            'project_image': '/projects/:id/images/:id/',
            'apps': '/projects/:id/apps/',
            'app': '/projects/:id/apps/:id/',
            'app_sections': '/projects/:id/apps/:id/sections/',
            'app_section': '/projects/:id/apps/:id/sections/:id/',
            'app_images': '/projects/:id/apps/:id/images/',
            'app_image': '/projects/:id/apps/:id/images/:id/',
            'snippets': '/projects/:id/code/',
            'snippet': '/projects/:id/code/:id/',
        }}
    ]
    if request.user.is_superuser:
        data[1]['auth'] = True

    return Response(data)
