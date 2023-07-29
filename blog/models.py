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

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        posts = self.posts.all()
        if posts.exists():
            posts.delete()
        return super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower().replace(' ', '-')
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
    related = models.ManyToManyField('self', blank=True, symmetrical=True)

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

        if self.image:
            path = os.path.join(MEDIA_ROOT, self.image.name)
            if os.path.exists(path):
                os.remove(path)

        if self.contents.all().exists():
            self.contents.all().delete()

        return super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

CONTENT_TYPES = [
    ('subtitle', 'Subtitle'),
    ('paragraph', 'Paragraph'),
    ('link', 'Link'),
    ('image', 'Image'),
    ('video', 'Video'),
    ('snippet', 'Code Snippet'),
]

class Content(models.Model):
    def get_image_path(instance, filename=None):
        return f'blog/images/{filename}'
    
    def get_video_path(instance, filename=None):
        return f'blog/videos/{filename}'

    type = models.CharField(choices=CONTENT_TYPES, max_length=20)
    order = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='contents')

    text = models.TextField(null=True, blank=True)
    text_alt = models.TextField(null=True, blank=True)
    href = models.URLField(null=True, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=100, null=True, blank=True)
    style = models.CharField(choices=STYLE_CHOICES, max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    video = models.FileField(upload_to=get_video_path, null=True, blank=True)

    def __str__(self):
        return f'{self.order} {self.type}'

    def delete(self, *args, **kwargs):
        if self.image:
            path = os.path.join(MEDIA_ROOT, self.image.name)
            if os.path.exists(path):
                os.remove(path)

        if self.video:
            path = os.path.join(MEDIA_ROOT, self.video.name)
            if os.path.exists(path):
                os.remove(path)

        return super().delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        if self.type == 'link':
            text_array = self.text.split()
            text_array[self.start] = f'<a href="{self.href}">' + text_array[self.start]
            text_array[self.end - 1] += '</a>'
            self.text_alt = text_array[0]
            for word in text_array[1:]:
                self.text_alt += f' {word}'

        if self.type == 'snippet':
            lexer = get_lexer_by_name(self.language)
            formatter = HtmlFormatter(style=self.style, full=False, noclasses=True)
            self.text_alt = highlight(self.text, lexer, formatter)

        if self.image:
            self.image = custom_img(self.image, 800, 2)

        if self.pk:
            prev_instance = Content.objects.filter(pk=self.pk)
            if prev_instance.exists():
                prev_instance = prev_instance[0]

                if prev_instance.image:
                    if (self.image and self.image != prev_instance.image) or self.type != 'image':
                        path = os.path.join(MEDIA_ROOT, prev_instance.image.name)
                        if os.path.exists(path):
                            os.remove(path)

                if prev_instance.video:
                    if (self.video and self.video != prev_instance.video) or self.type != 'video':
                        path = os.path.join(MEDIA_ROOT, prev_instance.video.name)
                        if os.path.exists(path):
                            os.remove(path)
            
        super().save(*args, **kwargs)
        return self

    class Meta:
        ordering = ['order']