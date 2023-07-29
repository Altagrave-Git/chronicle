from rest_framework.response import Response
from .serializers import CategorySerializer, PostSerializer, ContentSerializer
from .models import Category, Post, Content
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes, renderer_classes
from rest_framework import permissions
from rest_framework import status
from users.models import User
from rest_framework import parsers
from rest_framework import renderers



@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print(request.data)
        if request.user.is_superuser:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        if request.users.is_superuser:
            category = request.data.get('name')
            Category.objects.filter(name=category).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
        
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def posts_view(request, category):
    
    if request.method == 'GET':
        if category == 'all':
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

        else:
            try:
                category = Category.objects.get(name=category)
                posts = category.posts.all()
                serializer = PostSerializer(posts, many=True)
                return Response(serializer.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
    elif request.method == 'POST':
        if request.user.is_superuser:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    elif request.method == 'DELETE':
        if request.users.is_superuser:
            slug = request.data.get('slug')
            Post.objects.filter(slug=slug).delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
        
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def content_view(request, category, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:
        return Response(status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        content = post.contents.all()
        post = PostSerializer(post)
        content = ContentSerializer(content, many=True)

        data = {
            'post': post.data,
            'content': content.data
        }
        
        return Response(data)
    
    elif request.method == 'POST':
        if request.user.is_superuser:
            serializer = ContentSerializer(request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            pk = request.data.get('id')
            content = Content.objects.get(pk=pk).delete()
            content.delete()
            return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)