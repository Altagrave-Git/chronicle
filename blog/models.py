from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.urls import reverse
from django.template.defaultfilters import slugify
from datetime import datetime
from main.settings import MEDIA_ROOT
import os
from main.utils import custom_img
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        posts = self.posts.all()
        if posts.exists():
            posts.delete()
        return super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        return self
    
    class Meta:
        ordering = ['name']


class Post(models.Model):
    def get_image_path(instance, filename):
        return f'blog/thumbnail/{filename}'
    
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, null=True, blank=True, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    published = models.BooleanField(default=False)
    pub_date = models.DateField(null=True, blank=True)
    related = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        # delete previous image on overwrite
        if self.pk:
            try:
                prev_instance = Post.objects.get(pk=self.pk)
                self.slug = prev_instance.slug
                if self.image:
                    if prev_instance.image and self.image != prev_instance.image:
                        path = os.path.join(MEDIA_ROOT, prev_instance.image.name)
                        if os.path.exists(path):
                            os.remove(path)
                        self.image = custom_img(self.image, 800, (2/1))
            except: pass
        else:
            date_array = datetime.now().isoformat().split(sep="T")[0].split("-")
            self.slug = slugify(self.title) + f'-{date_array[2]}-{date_array[1]}-{date_array[0][2:]}'

            if self.image:
                self.image = custom_img(self.image, 800, (2/1))

        if self.published and not self.pub_date:
            self.pub_date = timezone.now()

        super().save(*args, **kwargs)
        return self
                        
    def delete(self, *args, **kwargs):

        all_children = [item for item in self.titles.all()
            ] + [item for item in self.paragraphs.all()
            ] + [item for item in self.snippets.all()
            ] + [item for item in self.images.all()
            ] + [item for item in self.videos.all()]
        
        for child in all_children: child.delete(deleting_related=True)
        
        if self.image:
            path = os.path.join(MEDIA_ROOT, self.image.name)
            if os.path.exists(path):
                os.remove(path)

        return super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

CONTENT_TYPES = [
    ('title', 'Title'),
    ('paragraph', 'Paragraph'),
    ('image', 'Image'),
    ('video', 'Video'),
    ('snippet', 'Code Snippet'),
]

CONTENT_SIZES = [
    ('xs', 'Extra Small'),
    ('s', 'Small'),
    ('m', 'Medium'),
    ('l', 'Large'),
    ('xl', 'Extra Large')
]

class Title(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='titles')
    type = models.CharField(choices=CONTENT_TYPES, default='title', max_length=20)
    order = models.IntegerField()

    text = models.CharField(max_length=200)
    size = models.CharField(choices=CONTENT_SIZES, max_length=2, default='m')

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        else:
            return self.text
    
    def save(self, recurse=True, *args, **kwargs):
        if recurse:
            post_content = [item for item in self.post.titles.filter(order__gte=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gte=self.order)] + [
                    item for item in self.post.snippets.filter(order__gte=self.order)] + [
                    item for item in self.post.images.filter(order__gte=self.order)] + [
                    item for item in self.post.videos.filter(order__gte=self.order)]
    
            if len(post_content):
                for item in post_content:
                    item.order += 1
                    item.save(recurse=False)

        super().save(*args, **kwargs)
        return self
    
    def delete(self, deleting_related=False, *args, **kwargs):
        if not deleting_related:
            post_content = [item for item in self.post.titles.filter(order__gt=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gt=self.order)] + [
                    item for item in self.post.snippets.filter(order__gt=self.order)] + [
                    item for item in self.post.images.filter(order__gt=self.order)] + [
                    item for item in self.post.videos.filter(order__gt=self.order)]

            if len(post_content):
                for item in post_content:
                    item.order -= 1
                    item.save()

        return super().delete(*args, **kwargs)
    

class Paragraph(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='paragraphs')
    type = models.CharField(choices=CONTENT_TYPES, default='paragraph', max_length=20)
    order = models.IntegerField()

    text = models.TextField()

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        else:
            return self.text
    
    def save(self, recurse=True, *args, **kwargs):
        if recurse:
            post_content = [item for item in self.post.titles.filter(order__gte=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gte=self.order)] + [
                    item for item in self.post.snippets.filter(order__gte=self.order)] + [
                    item for item in self.post.images.filter(order__gte=self.order)] + [
                    item for item in self.post.videos.filter(order__gte=self.order)]

            if len(post_content):
                for item in post_content:
                    item.order += 1
                    item.save(recurse=False)

        super().save(*args, **kwargs)
        return self
    
    def delete(self, deleting_related=False, *args, **kwargs):
        if not deleting_related:
            post_content = [item for item in self.post.titles.filter(order__gt=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gt=self.order)] + [
                    item for item in self.post.snippets.filter(order__gt=self.order)] + [
                    item for item in self.post.images.filter(order__gt=self.order)] + [
                    item for item in self.post.videos.filter(order__gt=self.order)]

            if len(post_content):
                for item in post_content:
                    item.order -= 1
                    item.save()

        return super().delete(*args, **kwargs)
    

class Snippet(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='snippets')
    type = models.CharField(choices=CONTENT_TYPES, default='snippet', max_length=20)
    order = models.IntegerField()

    title = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField()
    code = models.TextField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=100, null=True, blank=True)
    style = models.CharField(choices=STYLE_CHOICES, max_length=100, null=True, blank=True)

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        else:
            return self.text

    def save(self, recurse=True, *args, **kwargs):

        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter(style=self.style, full=False, noclasses=True)
        self.code = highlight(self.text, lexer, formatter)

        if recurse:
            post_content = [item for item in self.post.titles.filter(order__gte=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gte=self.order)] + [
                    item for item in self.post.snippets.filter(order__gte=self.order)] + [
                    item for item in self.post.images.filter(order__gte=self.order)] + [
                    item for item in self.post.videos.filter(order__gte=self.order)]
    
            if len(post_content):
                for item in post_content:
                    item.order += 1
                    item.save(recurse=False)

        super().save(*args, **kwargs)
        return self
    
    def delete(self, deleting_related=False, *args, **kwargs):
        if not deleting_related:
            post_content = [item for item in self.post.titles.filter(order__gt=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gt=self.order)] + [
                    item for item in self.post.snippets.filter(order__gt=self.order)] + [
                    item for item in self.post.images.filter(order__gt=self.order)] + [
                    item for item in self.post.videos.filter(order__gt=self.order)]

            if len(post_content):
                for item in post_content:
                    item.order -= 1
                    item.save()

        return super().delete(*args, **kwargs)
    

class Image(models.Model):
    def get_image_path(instance, filename=None):
        return f'blog/images/{filename}'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    type = models.CharField(choices=CONTENT_TYPES, default='image', max_length=20)
    order = models.IntegerField()

    image = models.ImageField(upload_to=get_image_path)
    text = models.TextField(null=True, blank=True)
    aspect = models.FloatField(default=2)
    max_width = models.IntegerField(default=800)

    def __str__(self):
        return self.image.name
    
    def save(self, recurse=True, *args, **kwargs):
        if self.pk:
            prev_instance = Image.objects.filter(pk=self.pk)
            if prev_instance.exists():
                prev_instance = prev_instance[0]

                if self.image.name != prev_instance.image.name:
                    path = os.path.join(MEDIA_ROOT, prev_instance.image.name)
                    if os.path.exists(path):
                        os.remove(path)

                    self.image = custom_img(self.image, self.max_width, self.aspect)
        else:
            self.image = custom_img(self.image, self.max_width, self.aspect)

        if recurse:
            post_content = [item for item in self.post.titles.filter(order__gte=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gte=self.order)] + [
                    item for item in self.post.snippets.filter(order__gte=self.order)] + [
                    item for item in self.post.images.filter(order__gte=self.order)] + [
                    item for item in self.post.videos.filter(order__gte=self.order)]
    
            if len(post_content):
                for item in post_content:
                    item.order += 1
                    item.save(recurse=False)
            
        super().save(*args, **kwargs)
        return self
    
    def delete(self, deleting_related=False, *args, **kwargs):

        path = os.path.join(MEDIA_ROOT, self.image.name)
        if os.path.exists(path):
            os.remove(path)

        if not deleting_related:
            post_content = [item for item in self.post.titles.filter(order__gt=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gt=self.order)] + [
                    item for item in self.post.snippets.filter(order__gt=self.order)] + [
                    item for item in self.post.images.filter(order__gt=self.order)] + [
                    item for item in self.post.videos.filter(order__gt=self.order)]

            if len(post_content):
                for item in post_content:
                    item.order -= 1
                    item.save()

        return super().delete(*args, **kwargs)
    

class Video(models.Model):
    def get_video_path(instance, filename=None):
        return f'blog/videos/{filename}'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='videos')
    type = models.CharField(choices=CONTENT_TYPES, default='video', max_length=20)
    order = models.IntegerField()

    video = models.FileField(upload_to=get_video_path)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.video.name
    
    def save(self, recurse=True, *args, **kwargs):
        if self.pk:
            prev_instance = Video.objects.filter(pk=self.pk)
            if prev_instance.exists():
                prev_instance = prev_instance[0]

                if self.video != prev_instance.video:
                    path = os.path.join(MEDIA_ROOT, prev_instance.video.name)
                    if os.path.exists(path):
                        os.remove(path)

        if recurse:
            post_content = [item for item in self.post.titles.filter(order__gte=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gte=self.order)] + [
                    item for item in self.post.snippets.filter(order__gte=self.order)] + [
                    item for item in self.post.images.filter(order__gte=self.order)] + [
                    item for item in self.post.videos.filter(order__gte=self.order)]
    
            if len(post_content):
                for item in post_content:
                    item.order += 1
                    item.save(recurse=False)
            
        super().save(*args, **kwargs)
        return self
    
    def delete(self, deleting_related=False, *args, **kwargs):

        path = os.path.join(MEDIA_ROOT, self.video.name)
        if os.path.exists(path):
            os.remove(path)

        if not deleting_related:
            post_content = [item for item in self.post.titles.filter(order__gt=self.order)] + [
                    item for item in self.post.paragraphs.filter(order__gt=self.order)] + [
                    item for item in self.post.snippets.filter(order__gt=self.order)] + [
                    item for item in self.post.images.filter(order__gt=self.order)] + [
                    item for item in self.post.videos.filter(order__gt=self.order)]

            if len(post_content):
                for item in post_content:
                    item.order -= 1
                    item.save()

        return super().delete(*args, **kwargs)