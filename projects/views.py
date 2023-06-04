from rest_framework.response import Response
from .serializers import ProjectSerializer, ProjectSectionSerializer, ProjectImageSerializer, SnippetSerializer
from .models import Project, ProjectSection, ProjectImage, Snippet
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework import permissions
from rest_framework import status
from users.models import User
from rest_framework import parsers


# CRUD for projects and project images
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@parser_classes([parsers.MultiPartParser, parsers.JSONParser, parsers.FormParser])
def projects(request):

    # GET all projects
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data)

    
    # POST a new project
    elif request.method == 'POST':
        print(request.FILES)
        if request.user.is_superuser:
            print(request.data)
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET a project
    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    # PUT a project
    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = ProjectSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE a project
    elif request.method == 'DELETE':
        if request.user.is_staff:
            project.images.all().delete()
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def project_sections(request, project_id):
    # GET all project sections
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        sections = project.sections.all()
        serializer = ProjectSectionSerializer(sections, many=True)
        return Response(serializer.data)
    
    # POST a new project section
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = ProjectSectionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def project_section(request, project_id, section_id):
    try:
        section = ProjectSection.objects.get(id=section_id)
    except ProjectSection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET a project section
    if request.method == 'GET':
        serializer = ProjectSectionSerializer(section)
        return Response(serializer.data)
    
    # PUT a project section
    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = ProjectSectionSerializer(section, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE a project section
    elif request.method == 'DELETE':
        if request.user.is_staff:
            section.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@parser_classes([parsers.FormParser, parsers.MultiPartParser])
def project_images(request, project_id):
    try: project = Project.objects.get(id=project_id)
    except: Response({"exception":"object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # GET all project images
    if request.method == 'GET':
        project_images = project.images.all()
        serializer = ProjectImageSerializer(project_images, many=True)
        return Response(serializer.data)
    
    # POST a new project image
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = ProjectImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def project_image(request, project_id, image_id):
    try:
        project_image = ProjectImage.objects.get(id=image_id)
    except ProjectImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET a project image
    if request.method == 'GET':
        serializer = ProjectImageSerializer(project_image)
        return Response(serializer.data)
    
    # PUT a project image
    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = ProjectImageSerializer(project_image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE a project image
    elif request.method == 'DELETE':
        if request.user.is_staff:
            project_image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def snippets(request, project_id):
    # GET all snippets
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        snippets = project.snippets.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    
    # POST a new snippet
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = SnippetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def snippet(request, project_id, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET a snippet
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    
    # PUT a snippet
    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = SnippetSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE a snippet
    elif request.method == 'DELETE':
        if request.user.is_staff:
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)