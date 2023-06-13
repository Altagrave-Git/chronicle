from rest_framework import serializers
from .models import Project, ProjectSection, ProjectImage, ProjectVideo, Snippet, Technology, LANGUAGE_CHOICES, STYLE_CHOICES


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)
    image = serializers.ImageField(allow_null=True, required=False)
    logo = serializers.FileField(allow_null=True, required=False)
    description = serializers.CharField(max_length=1000, allow_null=True, required=False)
    site = serializers.URLField(allow_null=True, allow_blank=True)
    repo = serializers.URLField(allow_null=True, allow_blank=True)
    tech = serializers.SerializerMethodField(allow_null=True, read_only=True)
    sections = serializers.SerializerMethodField(allow_null=True, read_only=True)
    images = serializers.SerializerMethodField(allow_null=True, read_only=True)
    videos = serializers.SerializerMethodField(allow_null=True, read_only=True)
    snippets = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_tech(self, obj):
        tech = TechnologySerializer(obj.tech.all(), many=True).data
        return tech

    def get_sections(self, obj):
        sections = ProjectSectionSerializer(obj.sections.all(), many=True).data
        return sections
    
    def get_images(self, obj):
        images = ProjectImageSerializer(obj.images.all(), many=True).data
        return images
    
    def get_videos(self, obj):
        videos = ProjectVideoSerializer(obj.videos.all(), many=True).data
        return videos
    
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
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'category', 'description', 'site', 'repo']

class ProjectSectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    type = serializers.ChoiceField(choices=ProjectSection.SECTION_TYPES)
    video = serializers.URLField(allow_null=True, required=False)
    order = serializers.IntegerField(default=0, allow_null=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    snippets = serializers.SerializerMethodField(allow_null=True, read_only=True)
    images = serializers.SerializerMethodField(allow_null=True, required=False)

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
        instance.video = validated_data.get('video', instance.video)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance
    
    class Meta:
        model = ProjectSection
        fields = ['id', 'title', 'description', 'project']


class ProjectImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    type = serializers.ChoiceField(choices=ProjectImage.TYPES)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=ProjectSection.objects.all())

    def create(self, validated_data):
        instance = ProjectImage.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.type = validated_data.get('type', instance.type)
        instance.project = validated_data.get('project', instance.project)
        instance.save()
        return instance
    
    class Meta:
        model = ProjectImage
        fields = ['image', 'project', 'type']


class ProjectVideoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    video = serializers.FileField()
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=ProjectSection.objects.all(), allow_null=True, required=False)

    def create(self, validated_data):
        instance = ProjectVideo.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.video = validated_data.get('video', instance.video)
        instance.project = validated_data.get('project', instance.project)
        instance.section = validated_data.get('section', instance.section)
        instance.save()
        return instance
    
    class Meta:
        model = ProjectVideo
        fields = ['title', 'video', 'project', 'section']


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), allow_null=True, required=False)
    project_section = serializers.PrimaryKeyRelatedField(queryset=ProjectSection.objects.all(), allow_null=True, required=False)
    title = serializers.CharField(required=False, allow_null=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    highlighted = serializers.CharField(read_only=True)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='monokai')

    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.project_section = validated_data.get('project_section', instance.project_section)
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
    
    class Meta:
        model = Snippet
        fields = ['id', 'project', 'project_section', 'title', 'code', 'highlighted', 'language', 'style']


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