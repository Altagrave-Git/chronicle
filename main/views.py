from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import renderers, parsers, permissions
import os


@api_view(['GET'])
@renderer_classes([renderers.TemplateHTMLRenderer, renderers.JSONRenderer])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def index(request):
    data = {
            'message': 'Welcome to Chronicle API',
            'project_endpoints': {
                'projects': '/projects/',
                'project': '/projects/:id/',
                'sections': '/projects/:id/sections/',
                'section': '/projects/:id/sections/:id/',
                'snippets': '/projects/:id/code/',
                'snippet': '/projects/:id/code/:id/',
                'images': '/projects/:id/images/',
                'image': '/projects/:id/images/:id/',
                'videos': '/projects/:id/videos/',
                'video': '/projects/:id/videos/:id',
                'tech': '/projects/:id/tech/'   
            },
            'blog_endpoints': {
                'categories': '/blog/',
                'category': '/blog/:slug/',
                'posts': '/blog/:slug/posts/',
                'post': '/blog/:slug/posts/:slug/',
                'contents': '/blog/:slug/posts/:slug/:type/',
                'content': '/blog/:slug/posts/:slug/:type/:id/',
                'related': '/blog/:slug/posts/:slug/related/',
            }
        }

    return Response(data=data, template_name='index.html')
