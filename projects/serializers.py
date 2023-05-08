from rest_framework import serializers
from .models import Project, App, ProjectImage

class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    site = serializers.URLField()
    repo = serializers.URLField()
    apps = serializers.SerializerMethodField(allow_null=True, read_only=True)
    images = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_apps(self, obj):
        apps = AppSerializer(obj.apps.all(), many=True).data
        return apps
    
    def get_images(self, obj):
        images = ProjectImageSerializer(obj.images.all(), many=True).data
        return images

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.site = validated_data.get('site', instance.site)
        instance.repo = validated_data.get('repo', instance.repo)
        instance.save()
        return instance
    
    class Meta:
        model = Project
        fields = ['name', 'category', 'description', 'site', 'repo']

class AppSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    site = serializers.URLField()
    project = serializers.CharField(max_length=100)
    images = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_images(self, obj):
        images = ProjectImageSerializer(obj.images.all(), many=True).data
        return images

    def create(self, validated_data):
        return App.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.site = validated_data.get('site', instance.site)
        instance.project = validated_data.get('project', instance.project)
        instance.save()
        return instance
    
    class Meta:
        model = App
        fields = ['name', 'category', 'description', 'site', 'project']

class ProjectImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    project = serializers.CharField(max_length=100)
    app = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return ProjectImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.project = validated_data.get('project', instance.project)
        instance.app = validated_data.get('app', instance.app)
        instance.save()
        return instance
    
    class Meta:
        model = ProjectImage
        fields = ['image', 'project', 'app']