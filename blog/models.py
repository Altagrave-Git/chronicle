from typing import Any, Iterable, Optional, Set
from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.urls import reverse
from django.template.defaultfilters import slugify
from datetime import datetime

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Post(models.Model):
    def get_image_path(instance, filename):
        return f'blog/{instance.title}/thumbnail/{filename}'
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    content = models.ManyToManyField('blog.Content', blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):

        date_array = datetime.now().isoformat().split(sep="T")[0].split("-")
        self.slug = slugify(self.title) + f'-{date_array[2]}-{date_array[1]}-{date_array[0][2:]}'
        super().save(*args, **kwargs)
        return self
    
    class Meta:
        ordering = ['-timestamp']


class Subtitle(models.Model):
    text = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            content = self.content.all()[0]
            content.order = self.order
            content.save()
        except:
            content = Content(type='subtitle', order=self.order, subtitle=self)
            content.save()
        return self


class Paragraph(models.Model):
    text = models.CharField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            content = self.content.all()[0]
            content.order = self.order
            content.save()
        except:
            content = Content(type='paragraph', order=self.order, paragraph=self)
            content.save()
        return self


class Link(models.Model):
    text = models.CharField(max_length=200)
    href = models.URLField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return self.href
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            content = self.content.all()[0]
            content.order = self.order
            content.save()
        except:
            content = Content(type='link', order=self.order, link=self)
            content.save()
        return self
    

class Snippet(models.Model):
    code = models.TextField()
    highlighted = models.TextField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='monokai', max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()
        
    def __str__(self):
        return f'code {self.pk}'

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter(style=self.style, full=False, noclasses=True)
        self.highlighted = highlight(self.code, lexer, formatter)   
        super().save(*args, **kwargs)
        try:
            content = self.content.all()[0]
            content.order = self.order
            content.save()
        except:
            content = Content(type='snippet', order=self.order, snippet=self)
            content.save()
        return self


class Image(models.Model):
    def get_image_path(instance, filename):
        return f'blog/{instance.post.pk}/images/{filename}'
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_image_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    order = models.IntegerField()

    def __str__(self):
        return f'image {self.pk}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            content = self.content.all()[0]
            content.order = self.order
            content.save()
        except:
            content = Content(type='image', order=self.order, image=self)
            content.save()
        return self


class Video(models.Model):
    def get_video_path(instance, filename):
        return f'blog/{instance.post.pk}/videos/{filename}'

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    video = models.FileField(upload_to=get_video_path, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            content = self.content.all()[0]
            content.order = self.order
            content.save()
        except:
            content = Content(type='video', order=self.order, video=self)
            content.save()
        return self


CONTENT_TYPES = [
    ('subtitle', 'Subtitle'),
    ('paragraph', 'Paragraph'),
    ('image', 'Image'),
    ('video', 'Video'),
    ('snippet', 'Code Snippet'),
]

class Content(models.Model):
    type = models.CharField(choices=CONTENT_TYPES, max_length=20)
    order = models.IntegerField(default=0)
    
    subtitle = models.ForeignKey(Subtitle, on_delete=models.CASCADE, null=True, blank=True, related_name='content')
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, null=True, blank=True, related_name='content')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, related_name='content')
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, null=True, blank=True, related_name='content')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True, related_name='content')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True, related_name='content')

    def __str__(self):
        return self.type

    def save(self, *args, **kwargs):
        super(Content, self).save(*args, **kwargs)
        for field in [self.subtitle, self.paragraph, self.link, self.snippet, self.image, self.video]:
            if field:
                field.post.content.add(self)
                break
        return self
            
    class Meta:
        ordering = ['order']