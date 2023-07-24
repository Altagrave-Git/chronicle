from rest_framework import serializers
from .models import Category, Post, Content, Subtitle, Paragraph, Link, Snippet, Image, Video, LANGUAGE_CHOICES, STYLE_CHOICES, CONTENT_TYPES


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField(max_length=1000, allow_null=True, required=False)
    image = serializers.ImageField(allow_null=True, required=False)
    timestamp = serializers.DateTimeField(read_only=True, format="%b %-d, %Y")
    published = serializers.BooleanField(allow_null=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

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


class SubtitleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=200)
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='slug')

    def create(self, validated_data):
        return super().create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.post = validated_data.get('post', instance.post)

    class Meta:
        model = Subtitle
        fields = ['id', 'text']


class ParagraphSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=1000)
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='slug')

    def create(self, validated_data):
        return Paragraph.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.post = validated_data.get('post', instance.post)
        instance.save()
        return instance
    
    class Meta:
        model = Paragraph
        fields = ['id', 'text']


class LinkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=200)
    href = serializers.URLField()
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='slug')

    def create(self, validated_data):
        return Link.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.href = validated_data.get('href', instance.href)
        instance.post = validated_data.get('post', instance.post)
        instance.save()
        return instance
    
    class Meta:
        model = Link
        fields = ['id', 'text', 'href']


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    highlighted = serializers.CharField(read_only=True)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='monokai')
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='slug')

    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.post = validated_data.get('post', instance.post)
        instance.save()
        return instance
    
    class Meta:
        model = Snippet
        fields = ['id', 'code', 'highlighted', 'language', 'style']


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    image = serializers.ImageField()
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='slug')

    def create(self, validated_data):
        return Image.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.post = validated_data.get('post', instance.post)
        instance.save()
        return instance
    
    class Meta:
        model = Image
        fields = ['id', 'title', 'image']


class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=1000)
    description = serializers.CharField(max_length=1000)
    video = serializers.FileField()
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='slug')

    def create(self, validated_data):
        return Video.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.video = validated_data.get('video', instance.video)
        instance.post = validated_data.get('post', instance.post)
        instance.save()
        return instance
    
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video']


class ContentSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=CONTENT_TYPES)
    order = serializers.IntegerField()
    content = serializers.SerializerMethodField()
    
    subtitle = serializers.PrimaryKeyRelatedField(queryset=Subtitle.objects.all(), allow_null=True, required=False)
    paragraph = serializers.PrimaryKeyRelatedField(queryset=Paragraph.objects.all(), allow_null=True, required=False)
    link = serializers.PrimaryKeyRelatedField(queryset=Link.objects.all(), allow_null=True, required=False)
    snippet = serializers.PrimaryKeyRelatedField(queryset=Snippet.objects.all(), allow_null=True, required=False)
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), allow_null=True, required=False)
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Content
        fields = '__all__'
        