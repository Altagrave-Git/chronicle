from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import renderers, parsers, permissions


@api_view(['GET'])
@renderer_classes([renderers.BrowsableAPIRenderer, renderers.JSONRenderer])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def index(request):
    data = [
        'Hello, welcome to Chronicle API',
        {
            'project endpoints': {
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
            }},
        {
            'blog endpoints': {
                'categories': '/blog/',
                'category': '/blog/:category/',
                'posts': '/blog/:category/posts/',
                'post': '/blog/:category/posts/:slug/',
                'contents': '/blog/:category/posts/:slug/:type/',
                'content': '/blog/:category/posts/:slug/:type/:id/',
                'related': '/blog/:category/posts/:slug/related/',
                'change_related': '/blog/:category/posts/:slug/related/:id/'
            }
        }
    ]

    return Response(data)
