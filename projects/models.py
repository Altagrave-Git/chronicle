from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from main.utils import custom_img
from main.settings import MEDIA_ROOT
import os
import shutil


class Technology(models.Model):
    tech = models.CharField(max_length=100)

    def __str__(self):
        return self.tech
    
    class Meta:
        ordering = ['tech']


class Project(models.Model):
    def get_image_path(instance, filename):
        return f'projects/{instance.name.replace(" ", "-")}/thumbnail/{filename}'
    
    def get_svg_path(instance, filename):
        return f'projects/{instance.name.replace(" ", "-")}/logo/{filename}'
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    tech = models.ManyToManyField(Technology, related_name='projects', blank=True)
    site = models.URLField(blank=True, null=True)
    repo = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to=get_image_path, default='projects/default.png')
    logo = models.FileField(upload_to=get_svg_path, null=True, blank=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name.replace(" ", "-")
    
    def save(self, *args, **kwargs):

        if self.pk:
            try:
                prev_instance = Project.objects.get(pk=self.pk)
                if self.image:
                    if self.image != prev_instance.image:
                        self.image = custom_img(self.image, 600, 16/9)
                        
                    if prev_instance.image and self.image != prev_instance.image:
                        path = os.path.join(MEDIA_ROOT, prev_instance.image)
                        if os.path.exists(path):
                            os.remove(path)


                if self.logo:
                    if prev_instance.logo and self.logo != prev_instance.logo:
                        path = os.path.join(MEDIA_ROOT, prev_instance.logo)
                        if os.path.exists(path):
                            os.remove(path)
            except: pass
        else:
            if self.image:
                self.image = custom_img(self.image, 600, (16/9))

        super().save(*args, **kwargs)
        return self


    def delete(self, *args, **kwargs):
        project_dir = os.path.join(MEDIA_ROOT, f'projects/{self.name.replace(" ", "-")}')
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        return super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['order', 'name']


class ProjectSection(models.Model):
    SECTION_TYPES = (
        ('text', 'Text'),
        ('list', 'List'),
        ('table', 'Table'),
        ('other', 'Other')
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=100, choices=SECTION_TYPES, default='text')
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.project.name + ' - ' + self.title
    
    class Meta:
        ordering = ['project', 'order']


class ProjectImage(models.Model):
    def get_image_path(instance, filename):
        return f'projects/{instance.project.name}/images/{filename}'
    
    TYPES = (
        ('desktop-display', 'Desktop Display'),
        ('mobile-display', 'Mobile Display'),
        ('logo', 'Logo'),
        ('other', 'Other')
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, default='projects/default.png')
    type = models.CharField(max_length=20, choices=TYPES, default='other')

    def __str__(self):
        return self.project.name + ' - ' + str(self.image)
    
    def save(self, *args, **kwargs):

        if self.pk:
            prev_instance = ProjectImage.objects.filter(pk=self.pk)
            if prev_instance.exists():
                prev_instance = prev_instance[0]
                if self.image != prev_instance.image:
                    self.image = custom_img(self.image)

                if prev_instance.image and self.image != prev_instance.image:
                    if (self.image and self.image != prev_instance.image) or self.type != 'image':
                        path = os.path.join(MEDIA_ROOT, prev_instance.image)
                        if os.path.exists(path):
                            os.remove(path)
        else:
            if self.image:
                self.image = custom_img(self.image)

        super().save(*args, **kwargs)
        return self
    
    def delete(self, *args, **kwargs):
        if self.image:
            path = os.path.join(MEDIA_ROOT, self.image)
            if os.path.exists(path):
                os.remove(path)

        return super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['project', 'section']


class ProjectVideo(models.Model):
    def get_video_path(instance, filename):
        return f'projects/{instance.project.name.replace(" ", "-")}/videos/{filename}'

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    video = models.FileField(upload_to=get_video_path, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)

    def __str__(self):
        return self.project.name + '//' + self.title
    
    def save(self, *args, **kwargs):
    
        if self.pk:
            prev_instance = ProjectVideo.objects.filter(pk=self.pk)
            if prev_instance.exists():
                prev_instance = prev_instance[0]

                if prev_instance.video and self.video != prev_instance.video:
                    path = os.path.join(MEDIA_ROOT, prev_instance.video)
                    if os.path.exists(path):
                        os.remove(path)

        super().save(*args, **kwargs)
        return self
    
    def delete(self, *args, **kwargs):
        if self.video:
            path = os.path.join(MEDIA_ROOT, self.video)
            if os.path.exists(path):
                os.remove(path)

        return super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['project', 'section', 'title']


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    project = models.ForeignKey(Project, related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
    project_section = models.ForeignKey(ProjectSection, related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    highlighted = models.TextField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='monokai', max_length=100)

    class Meta:
        ordering = ['project', 'project_section']
        
    def __str__(self):
        if self.project_section:
            return f'{self.project} - {self.project_section} - {self.title}'
        elif self.project:
            return f'{self.project} - {self.title}'
        
        return self.title

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter(style=self.style, full=False, noclasses=True)
        self.highlighted = highlight(self.code, lexer, formatter)   
        super().save(*args, **kwargs)