from rest_framework.response import Response
from .serializers import CategorySerializer, PostSerializer
from .models import Category, Post, Content, Subtitle, Paragraph, Link, Snippet, Image, Video
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes, renderer_classes
from rest_framework import permissions
from rest_framework import status
from users.models import User
from rest_framework import parsers
from rest_framework import renderers
# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
def blog_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        categories = Category.objects.all()
        return 



@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@parser_classes([parsers.JSONParser, parsers.FormParser])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
def post_view(request, category):
    if request.method == 'GET':
        return