from typing import Any, Iterable, Optional
from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.urls import reverse
from django.template.defaultfilters import slugify

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    def get_image_path(instance, filename):
        return f'blog/{instance.title}/thumbnail/{filename}'
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    
    class Meta:
        ordering = ['-timestamp']


class Subtitle(models.Model):
    text = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        
        return super().save(*args, **kwargs)


class Paragraph(models.Model):
    text = models.CharField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Link(models.Model):
    text = models.CharField(max_length=200)
    href = models.URLField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.href
    

class Snippet(models.Model):
    code = models.TextField()
    highlighted = models.TextField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='monokai', max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.pk

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter(style=self.style, full=False, noclasses=True)
        self.highlighted = highlight(self.code, lexer, formatter)   
        super().save(*args, **kwargs)


class Image(models.Model):
    def get_image_path(instance, filename):
        return f'blog/{instance.post.pk}/images/{filename}'
    
    image = models.ImageField(upload_to=get_image_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.pk


class Video(models.Model):
    def get_video_path(instance, filename):
        return f'blog/{instance.post.pk}/videos/{filename}'

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    video = models.FileField(upload_to=get_video_path, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Content(models.Model):
    CONTENT_TYPES = [
        ('title', 'Title'),
        ('paragraph', 'Paragraph'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('snippet', 'Code Snippet'),
    ]

    type = models.CharField(choices=CONTENT_TYPES, max_length=20)
    order = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    subtitle = models.ForeignKey(Subtitle, on_delete=models.CASCADE, null=True, blank=True)
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, null=True, blank=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['order']