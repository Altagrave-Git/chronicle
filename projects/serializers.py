from rest_framework import serializers
from .models import Project, ProjectSection, ProjectImage, App, AppSection, AppImage, Snippet, Technology, LANGUAGE_CHOICES, STYLE_CHOICES

class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, allow_null=True)
    tech = serializers.SerializerMethodField(allow_null=True, read_only=True)
    site = serializers.URLField(allow_null=True)
    repo = serializers.URLField(allow_null=True)
    sections = serializers.SerializerMethodField(allow_null=True, read_only=True)
    apps = serializers.SerializerMethodField(allow_null=True, read_only=True)
    images = serializers.SerializerMethodField(allow_null=True, read_only=True)
    snippets = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_tech(self, obj):
        tech = TechnologySerializer(obj.tech.all(), many=True).data
        return tech

    def get_sections(self, obj):
        sections = ProjectSectionSerializer(obj.sections.all(), many=True).data
        return sections

    def get_apps(self, obj):
        apps = AppSerializer(obj.apps.all(), many=True).data
        return apps
    
    def get_images(self, obj):
        images = ProjectImageSerializer(obj.images.all(), many=True).data
        return images
    
    def get_snippets(self, obj):
        snippets = SnippetSerializer(obj.snippets.all(), many=True).data
        return snippets

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

class ProjectSectionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    project = serializers.CharField(max_length=100)
    images = serializers.SerializerMethodField(allow_null=True)
    type = serializers.ChoiceField(choices=ProjectSection.SECTION_TYPES)
    order = serializers.IntegerField(default=0, allow_null=True)
    snippets = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_snippets(self, obj):
        snippets = SnippetSerializer(obj.snippets.all(), many=True).data
        return snippets

    def get_images(self, obj):
        images = ProjectImageSerializer(obj.images.all(), many=True).data
        return images

    def create(self, validated_data):
        return ProjectSection.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.project = validated_data.get('project', instance.project)
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance
    
    class Meta:
        model = ProjectSection
        fields = ['title', 'description', 'project']


class ProjectImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    project = serializers.CharField(max_length=100)
    section = serializers.CharField(max_length=100, allow_null=True)
    type = serializers.ChoiceField(choices=ProjectImage.TYPES)

    def create(self, validated_data):
        return ProjectImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.project = validated_data.get('project', instance.project)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance
    
    class Meta:
        model = ProjectImage
        fields = ['image', 'project', 'app']


class AppSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    site = serializers.URLField()
    project = serializers.CharField(max_length=100)
    sections = serializers.SerializerMethodField(allow_null=True, read_only=True)
    images = serializers.SerializerMethodField(allow_null=True, read_only=True)
    snippets = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_snippets(self, obj):
        snippets = SnippetSerializer(obj.snippets.all(), many=True).data
        return snippets

    def get_sections(self, obj):
        sections = AppSectionSerializer(obj.sections.all(), many=True).data
        return sections

    def get_images(self, obj):
        images = AppImageSerializer(obj.images.all(), many=True).data
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


class AppSectionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    app = serializers.CharField(max_length=100)
    images = serializers.SerializerMethodField(allow_null=True)
    type = serializers.ChoiceField(choices=AppSection.SECTION_TYPES)
    order = serializers.IntegerField(default=0, allow_null=True)
    snippets = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_snippets(self, obj):
        snippets = SnippetSerializer(obj.snippets.all(), many=True).data
        return snippets

    def get_images(self, obj):
        images = AppImageSerializer(obj.images.all(), many=True).data
        return images

    def create(self, validated_data):
        return AppSection.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.app = validated_data.get('app', instance.app)
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance
    
    class Meta:
        model = AppSection
        fields = ['title', 'description', 'app']


class AppImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    app = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=AppImage.TYPES)

    def create(self, validated_data):
        return AppImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.app = validated_data.get('app', instance.app)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance
    
    class Meta:
        model = AppImage
        fields = ['image', 'app', 'type']


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    project = serializers.CharField(max_length=100, required=False, allow_blank=True)
    project_section = serializers.CharField(max_length=100, required=False, allow_blank=True)
    app = serializers.CharField(max_length=100, required=False, allow_blank=True)
    app_section = serializers.CharField(max_length=100, required=False, allow_blank=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    highlighted = serializers.CharField(read_only=True)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='monokai')

    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.project_section = validated_data.get('project_section', instance.project_section)
        instance.app = validated_data.get('app', instance.app)
        instance.app_section = validated_data.get('app_section', instance.app_section)
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
    
    class Meta:
        model = Snippet
        fields = ['id', 'project', 'project_section', 'app', 'app_section', 'title', 'code', 'highlighted', 'language', 'style']


class TechnologySerializer(serializers.Serializer):
    tech = serializers.CharField(max_length=100)

    def get_projects(self, obj):
        projects = ProjectSerializer(obj.projects.all(), many=True).data
        return projects

    def create(self, validated_data):
        return Technology.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.tech = validated_data.get('tech', instance.tech)
        instance.save()
        return instance
    
    class Meta:
        model = Technology
        fields = ['tech']