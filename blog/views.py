from rest_framework.response import Response
from .serializers import CategorySerializer, PostSerializer, ContentSerializer, TitleSerializer, ParagraphSerializer, SnippetSerializer, ImageSerializer, VideoSerializer
from .models import Category, Post, Title, Paragraph, Snippet, Image, Video, STYLE_CHOICES, LANGUAGE_CHOICES
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes, renderer_classes
from rest_framework import parsers, renderers, permissions, status
from users.models import User



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
            return Response(status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def category_view(request, category):
    try:
        instance = Category.objects.get(slug=category)
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
            return Response(status.HTTP_401_UNAUTHORIZED)
    
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
                return Response(status.HTTP_404_NOT_FOUND)
            
    elif request.method == 'POST':
        if request.user.is_superuser:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
        
    elif request.method == 'DELETE':
        if request.users.is_superuser:
            slug = request.data.get('slug')
            Post.objects.filter(slug=slug).delete()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
        
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


TYPE_METHODS = {
    'title': [Title, TitleSerializer],
    'paragraph': [Paragraph, ParagraphSerializer],
    'snippet': [Snippet, SnippetSerializer],
    'image': [Image, ImageSerializer],
    'video': [Video, VideoSerializer]
}


@api_view(['GET', 'PUT', 'DELETE'])
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
    
    elif request.method == 'PUT':
        if request.user.is_superuser:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        if request.user.is_superuser:
            category = post.category
            post.delete()
            if not category.posts.all().exists():
                category.delete()
            return Response(status.HTTP_200_OK)

    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


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
        return Response(status.HTTP_404_NOT_FOUND)
    
    
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
            return Response(status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET'])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def related_view(request, category, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = { 'related': [], 'unrelated': [] }
        related = post.related.all()
        exclusions = [post.id]

        if related.exists():
            exclusions += [item.id for item in related]
            data['related'] = PostSerializer(related, many=True).data

        unrelated = Post.objects.exclude(id__in=exclusions)

        if unrelated.exists():
            data['unrelated'] = PostSerializer(unrelated, many=True).data

        return Response(data)
    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['POST', 'PUT'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@parser_classes([parsers.JSONParser])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
def change_related_view(request, category, slug, id):
    try:
        post = Post.objects.get(slug=slug)
        related = Post.objects.get(id=id)
    except:
        return Response(status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        if request.user.is_superuser:
            post.related.add(related)
            return Response(status.HTTP_200_OK)

        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
        
    elif request.method == 'PUT':
        if request.user.is_superuser:
            post.related.remove(related)
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)

    else:
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)