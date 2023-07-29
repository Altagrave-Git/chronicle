from rest_framework import serializers
from .models import Category, Post, Content, LANGUAGE_CHOICES, STYLE_CHOICES, CONTENT_TYPES


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
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
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('name', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.published = validated_data.get('published', instance.published)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class ContentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.ChoiceField(choices=CONTENT_TYPES)
    order = serializers.IntegerField()
    post = serializers.SlugRelatedField(queryset=Post.objects.all(), slug_field='slug')

    text = serializers.CharField(allow_null=True, required=False)
    text_alt = serializers.CharField(allow_null=True, required=False)
    href = serializers.URLField(allow_null=True, required=False)
    start = serializers.IntegerField(allow_null=True, required=False)
    end = serializers.IntegerField(allow_null=True, required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, allow_null=True, required=False)
    style = serializers.ChoiceField(choices=STYLE_CHOICES, allow_null=True, required=False)
    image = serializers.ImageField(allow_null=True, required=False)
    video = serializers.FileField(allow_null=True, required=False)

    def create(self, validated_data):
        content_type = validated_data.get('type')

        if content_type == 'paragraph' or content_type == 'subtitle':
            if 'text' not in validated_data:
                raise serializers.ValidationError(f'text field is required for type: {content_type}')
        
        if content_type == 'link':
            if 'text' not in validated_data or 'href' not in validated_data or 'start' not in validated_data or 'end' not in validated_data:
                raise serializers.ValidationError("text, href, start and end are required for type: link")

        if content_type == 'snippet':
            if 'text' not in validated_data or 'language' not in validated_data or 'style' not in validated_data:
                raise serializers.ValidationError("text, language, and style are required for type: snippet")
            
        if content_type == 'image':
            if 'image' not in validated_data:
                raise serializers.ValidationError('image field is required for type: image')
            
        if content_type == 'video':
            if 'video' not in validated_data:
                raise serializers.ValidationError('video field is required for type: video')

        return Content.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        content_type = validated_data.get('type')

        if content_type == 'paragraph' or content_type == 'subtitle':
            if 'text' not in validated_data:
                raise serializers.ValidationError(f'text field is required for type: {content_type}')
        
        if content_type == 'link':
            if 'text' not in validated_data or 'href' not in validated_data or 'start' not in validated_data or 'end' not in validated_data:
                raise serializers.ValidationError("text, href, start and end are required for type: link")

        if content_type == 'snippet':
            if 'text' not in validated_data or 'language' not in validated_data or 'style' not in validated_data:
                raise serializers.ValidationError("text, language, and style are required for type: snippet")
            
        if content_type == 'image':
            if 'image' not in validated_data:
                raise serializers.ValidationError('image field is required for type: image')
            
        if content_type == 'video':
            if 'video' not in validated_data:
                raise serializers.ValidationError('video field is required for type: video')
            
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)
        instance.post = validated_data.get('post', instance.post)
        instance.text = validated_data.get('text', instance.text)
        instance.text_alt = validated_data.get('text_alt', instance.text_alt)
        instance.href = validated_data.get('href', instance.href)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.image = validated_data.get('image', instance.image)
        instance.video = validated_data.get('video', instance.video)
        instance.save()
        return instance
    