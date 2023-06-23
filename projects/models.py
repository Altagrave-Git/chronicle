from django.db import models
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


class Technology(models.Model):
    tech = models.CharField(max_length=100)

    def __str__(self):
        return self.tech
    
    class Meta:
        ordering = ['tech']


class Project(models.Model):
    def get_image_path(instance, filename):
        return f'projects/{instance.name}/thumbnail/{filename}'
    
    def get_svg_path(instance, filename):
        return f'projects/{instance.name}/logo/{filename}'
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    tech = models.ManyToManyField(Technology, related_name='projects')
    site = models.URLField(blank=True, null=True)
    repo = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to=get_image_path, default='projects/default.png')
    logo = models.FileField(upload_to=get_svg_path, null=True, blank=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name.replace(" ", "-")
    
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
    
    class Meta:
        ordering = ['project', 'section']


class ProjectVideo(models.Model):
    def get_video_path(instance, filename):
        return f'projects/{instance.project.name}/videos/{filename}'

    title = models.CharField(max_length=100)
    video = models.FileField(upload_to=get_video_path, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)

    def __str__(self):
        return self.project.name + '//' + self.title
    
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


