from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.sessions.models import Session


@api_view(['GET'])
def index(request):
    data = [
        'Hello, welcome to Chronicle API',
        {
        'endpoints': {
            'projects': '/projects/',
            'project': '/projects/:id/',
            'project_sections': '/projects/:id/sections/',
            'project_section': '/projects/:id/sections/:id/',
            'project_images': '/projects/:id/images/',
            'project_image': '/projects/:id/images/:id/',
            'snippets': '/projects/:id/code/',
            'snippet': '/projects/:id/code/:id/',
        }}
    ]

    return Response(data)
