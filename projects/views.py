from rest_framework.response import Response
from .serializers import ProjectSerializer, ProjectSectionSerializer, ProjectImageSerializer, AppSerializer, AppSectionSerializer, AppImageSerializer, SnippetSerializer
from .models import Project, ProjectSection, ProjectImage, App, AppSection, AppImage, Snippet
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework import status
from users.models import User


# CRUD for projects, apps, and project images
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def projects(request):
    # GET all projects
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data)

    
    # POST a new project
    elif request.method == 'POST':
        session = request.session.get("active_session")
        if session:
            user = User.objects.filter(active_session=session)[0]
        if user.is_superuser:
            print(request.POST)
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
            project.apps.all().delete()
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
@authentication_classes([])
def project_images(request, project_id):
    # GET all project images
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
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
def apps(request, project_id):
    # GET all apps
    if request.method == 'GET':
        project = Project.objects.get(id=project_id)
        apps = project.apps.all()
        serializer = AppSerializer(apps, many=True)
        return Response(serializer.data)
    
    # POST a new app
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = AppSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def app(request, project_id, app_id):
    try:
        app = App.objects.get(id=app_id)
    except App.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET an app
    if request.method == 'GET':
        serializer = AppSerializer(app)
        return Response(serializer.data)
    
    # PUT an app
    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = AppSerializer(app, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE an app
    elif request.method == 'DELETE':
        if request.user.is_staff:
            app.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def app_images(request, project_id, app_id):
    # GET all app images
    if request.method == 'GET':
        app = App.objects.get(id=app_id)
        app_images = app.images.all()
        serializer = AppImageSerializer(app_images, many=True)
        return Response(serializer.data)
    
    # POST a new app image
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = AppImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def app_image(request, project_id, app_id, image_id):
    try:
        app_image = AppImage.objects.get(id=image_id)
    except AppImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET an app image
    if request.method == 'GET':
        serializer = AppImageSerializer(app_image)
        return Response(serializer.data)
    
    # PUT an app image
    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = AppImageSerializer(app_image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE an app image
    elif request.method == 'DELETE':
        if request.user.is_staff:
            app_image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def app_sections(request, project_id, app_id):
    # GET all app sections
    if request.method == 'GET':
        app = App.objects.get(id=app_id)
        app_sections = app.sections.all()
        serializer = AppSectionSerializer(app_sections, many=True)
        return Response(serializer.data)
    
    # POST a new app section
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = AppSectionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
@authentication_classes([])
def app_section(request, project_id, app_id, section_id):
    try:
        app_section = AppSection.objects.get(id=section_id)
    except AppSection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET an app section
    if request.method == 'GET':
        serializer = AppSectionSerializer(app_section)
        return Response(serializer.data)
    
    # PUT an app section
    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = AppSectionSerializer(app_section, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE an app section
    elif request.method == 'DELETE':
        if request.user.is_staff:
            app_section.delete()
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