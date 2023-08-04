from rest_framework import serializers
from .models import Category, Post, Title, Paragraph, Snippet, Image, Video, LANGUAGE_CHOICES, STYLE_CHOICES, CONTENT_TYPES


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(read_only=True)
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.posts.all().count()

    def create(self, validated_data):
        instance = Category(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True, format="%b %-d, %Y")
    pub_date = serializers.DateField(read_only=True, format="%b %-d, %Y")

    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, allow_null=True, required=False)
    image = serializers.ImageField(allow_null=True, required=False)
    published = serializers.BooleanField(allow_null=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.category.name

    def create(self, validated_data):
        instance = Post(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.published = validated_data.get('published', instance.published)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class TitleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(choices=CONTENT_TYPES)
    order = serializers.IntegerField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    text = serializers.CharField(max_length=200)
    size = serializers.CharField(required=False)

    def create(self, validated_data):
        instance = Title(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        print(instance.id)

        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.post = validated_data.get('post', instance.post)
        instance.text = validated_data.get('text', instance.text)
        instance.size = validated_data.get('size', instance.size)
        instance.save()
        return instance
    

class ParagraphSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(choices=CONTENT_TYPES)
    order = serializers.IntegerField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    text = serializers.CharField()

    def create(self, validated_data):
        instance = Paragraph(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
    

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(choices=CONTENT_TYPES)
    order = serializers.IntegerField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    title = serializers.CharField(allow_null=True, required=False)
    text = serializers.CharField()
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    style = serializers.ChoiceField(choices=STYLE_CHOICES)
    code = serializers.CharField(read_only=True)

    def create(self, validated_data):
        instance = Snippet(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.text = validated_data.get('text', instance.text)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
    

class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(choices=CONTENT_TYPES)
    order = serializers.IntegerField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    image = serializers.ImageField(required=False)
    text = serializers.CharField(allow_null=True, required=False)
    aspect = serializers.FloatField(required=False)
    max_width = serializers.IntegerField(required=False)

    def create(self, validated_data):
        instance = Image(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.aspect = validated_data.get('aspect', instance.aspect)
        instance.max_width = validated_data.get('max_width', instance.max_width)
        instance.save()
        return instance
    

class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(choices=CONTENT_TYPES)
    order = serializers.IntegerField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    video = serializers.FileField(required=False)
    text = serializers.CharField(allow_null=True, required=False)

    def create(self, validated_data):
        instance = Video(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.video = validated_data.get('video', instance.video)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
    

class ContentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True, format="%b %-d, %Y")
    pub_date = serializers.DateField(read_only=True, format="%b %-d, %Y")

    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, allow_null=True, required=False)
    image = serializers.ImageField(allow_null=True, required=False)
    published = serializers.BooleanField(allow_null=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.SerializerMethodField()

    style_choices = serializers.SerializerMethodField()
    language_choices = serializers.SerializerMethodField()

    titles =  TitleSerializer(many=True, required=False)
    paragraphs = ParagraphSerializer(many=True, required=False)
    snippets = SnippetSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    videos = VideoSerializer(many=True, required=False)

    def get_category_name(self, obj):
        return obj.category.name
    
    def get_style_choices(self, obj):
        if obj.published == False:
            return STYLE_CHOICES
        else:
            return []
    
    def get_language_choices(self, obj):
        if not obj.published:
            return LANGUAGE_CHOICES
        else:
            return []