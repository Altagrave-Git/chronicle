from rest_framework.response import Response
from rest_framework import request
from rest_framework.decorators import api_view
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')




@api_view(['GET'])
def chronicle(request):
    data = [
        'Hello, welcome to chronicle API',
        {
            'auth': False
        },
        {
        'endpoints': {
            'main': '/api/',
            'projects': '/api/projects/',
            'project': '/api/projects/:id/',
            'project_sections': '/api/projects/:id/sections/',
            'project_section': '/api/projects/:id/sections/:id/',
            'project_images': '/api/projects/:id/images/',
            'project_image': '/api/projects/:id/images/:id/',
            'apps': '/api/projects/:id/apps/',
            'app': '/api/projects/:id/apps/:id/',
            'app_sections': '/api/projects/:id/apps/:id/sections/',
            'app_section': '/api/projects/:id/apps/:id/sections/:id/',
            'app_images': '/api/projects/:id/apps/:id/images/',
            'app_image': '/api/projects/:id/apps/:id/images/:id/',
            'snippets': '/api/projects/:id/code/',
            'snippet': '/api/projects/:id/code/:id/',
        }}
    ]
    if request.user.is_staff:
        data[1]['auth'] = True

    return Response(data)
