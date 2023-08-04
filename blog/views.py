from rest_framework.response import Response
from .serializers import CategorySerializer, PostSerializer, ContentSerializer, TitleSerializer, ParagraphSerializer, SnippetSerializer, ImageSerializer, VideoSerializer
from .models import Category, Post, Title, Paragraph, Snippet, Image, Video, STYLE_CHOICES, LANGUAGE_CHOICES
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes, renderer_classes
from rest_framework import permissions
from rest_framework import status
from users.models import User
from rest_framework import parsers
from rest_framework import renderers



@api_view(['GET', 'POST'])
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
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def category_view(request, category):
    try:
        instance = Category.objects.get(name=category)
    except:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(instance)
        data = serializer.data
        data['endpoints'] = ['/posts/']
        return Response(data)

    elif request.method == 'PUT':
        if request.user.is_superuser:
            serializer = CategorySerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            instance.delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
        
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    

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
                category = Category.objects.get(slug=category)
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


TYPE_METHODS = {
    'title': [Title, TitleSerializer],
    'paragraph': [Paragraph, ParagraphSerializer],
    'snippet': [Snippet, SnippetSerializer],
    'image': [Image, ImageSerializer],
    'video': [Video, VideoSerializer]
}


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def post_view(request, category, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:
        return Response(status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ContentSerializer(post)
        data = serializer.data
        data['endpoints'] = [f'/{key}/' for key in TYPE_METHODS]
        return Response(data)
            
    elif request.method == 'POST':
        if request.user.is_superuser:
            data = request.data
            content_methods = {
                'title': [Title, TitleSerializer],
                'paragraph': [Paragraph, ParagraphSerializer],
                'snippet': [Snippet, SnippetSerializer],
                'image': [Image, ImageSerializer],
                'video': [Video, VideoSerializer]
            }
            content_type = data.get('type')
            model = content_methods[content_type][0]
            serializer = content_methods[content_type][1]

            id = request.data.get('id')
            if id:
                instance = model.objects.get(id=id)
                serializer = serializer(instance, data=data)
            else:
                serializer = serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def contents_view(request, category, slug, type):

    [model, serializer] = TYPE_METHODS.get(type)

    if request.method == 'GET':
        post = Post.objects.get(slug=slug)
        content = model.objects.filter(post=post.id)
        serializer = serializer(content, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if request.user.is_superuser:
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def content_view(request, category, slug, type, id):

    [model, serializer] = TYPE_METHODS.get(type)

    try:
        content = model.objects.get(id=id)
        if content.post.slug != slug:
            return Response({'err_msg':'content, post mismatch'}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method == 'GET':
        return Response(serializer(content).data)
    
    elif request.method == 'PUT':
        if request.user.is_superuser:
            serializer = serializer(content, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            content.delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)