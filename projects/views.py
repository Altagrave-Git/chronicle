from rest_framework.response import Response
from .serializers import ProjectSerializer, AppSerializer, ProjectImageSerializer
from .models import Project, App, ProjectImage
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated


# CRUD for projects, apps, and project images
@api_view(['GET', 'POST'])
def projects(request):
    # GET all projects
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data)

    
    # POST a new project
    elif request.method == 'POST':
        if request.user.is_staff:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def project(request, project_name):
    try:
        project = Project.objects.get(name=project_name)
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
def apps(request, project_name):
    # GET all apps
    if request.method == 'GET':
        apps = App.objects.filter(project=project_name)
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
def app(request, project_name, app_name):
    try:
        app = App.objects.get(name=app_name)
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
def project_images(request, project_name):
    # GET all project images
    if request.method == 'GET':
        project_images = ProjectImage.objects.filter(project=project_name)
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
def project_image(request, project_name, image_id):
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
    