from rest_framework import serializers
from .models import Post, Section, Paragraph, Image, Video, Snippet, Link, LANGUAGE_CHOICES, STYLE_CHOICES


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    slug = serializers.CharField(read_only=True)
    category = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, allow_null=True, required=False)
    image = serializers.ImageField(allow_null=True, required=False)
    timestamp = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('name', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
    
    class Meta:
        model = Post
        fields = '__all__'


class SectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    order = serializers.IntegerField(allow_null=True, required=False)

    def create(self, validated_data):
        return Section.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.post = validated_data.get('post', instance.post)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance
    
    class Meta:
        model = Section
        fields = '__all__'


class ParagraphSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    text = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        return Paragraph.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.section = validated_data.get('section', instance.section)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
    
    class Meta:
        model = Paragraph
        fields = '__all__'


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), allow_null=True, required=False)
    paragraph = serializers.PrimaryKeyRelatedField(queryset=Paragraph.objects.all(), allow_null=True, required=False)

    def create(self, validated_data):
        return Image.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.post = validated_data.get('post', instance.post)
        instance.section = validated_data.get('section', instance.section)
        instance.paragraph = validated_data.get('paragraph', instance.paragraph)
        instance.save()
        return instance
    
    class Meta:
        model = Image
        fields = '__all__'


class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=1000)
    description = serializers.CharField(max_length=1000)
    video = serializers.FileField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    def create(self, validated_data):
        return Video.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.video = validated_data.get('video', instance.video)
        instance.post = validated_data.get('post', instance.post)
        instance.section = validated_data.get('section', instance.section)
        instance.save()
        return instance
    
    class Meta:
        model = Video
        fields = '__all__'


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_null=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    highlighted = serializers.CharField(read_only=True)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='monokai')
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), allow_null=True, required=False)
    order = serializers.IntegerField()

    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.section = validated_data.get('section', instance.section)
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance
    
    class Meta:
        model = Snippet
        fields = '__all__'


class LinkSerializer(serializers.Serializer):
    paragraph = serializers.PrimaryKeyRelatedField(queryset=Paragraph.objects.all())
    text = serializers.CharField(max_length=200)
    href = serializers.URLField()

    def create(self, validated_data):
        return Link.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.paragraph = validated_data.get('paragraph', instance.paragraph)
        instance.text = validated_data.get('text', instance.text)
        instance.href = validated_data.get('href', instance.href)
        instance.save()
        return instance
    
    class Meta:
        model = Link
        fields = '__all__'