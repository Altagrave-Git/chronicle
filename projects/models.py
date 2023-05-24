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
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    tech = models.ManyToManyField(Technology, related_name='projects')
    site = models.URLField(blank=True, null=True)
    repo = models.URLField(blank=True, null=True)
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
        return f'projects/{instance.project.name}/{filename}'
    
    TYPES = (
        ('mobile-display', 'Mobile Display'),
        ('desktop-display', 'Desktop Display'),
        ('mobile-screenshot', 'Mobile Screenshot'),
        ('desktop-screenshot', 'Desktop Screenshot'),
        ('logo', 'Logo'),
        ('other', 'Other')
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, default='projects/default.png')
    type = models.CharField(max_length=20, choices=TYPES, default='other')

    def __str__(self):
        if self.section:
            return self.project.name + ' - ' + self.section.title + ' - ' + str(self.image)
        else:
            return self.project.name + ' - ' + str(self.image)
    
    class Meta:
        ordering = ['project']


class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    site = models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='apps')

    def __str__(self):
        return self.project.name + ': ' + self.name
    
    class Meta:
        ordering = ['name']


class AppSection(models.Model):
    SECTION_TYPES = (
        ('list', 'List'),
        ('text', 'Text'),
        ('table', 'Table'),
        ('other', 'Other')
    )
        
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=100, choices=SECTION_TYPES, default='other')
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.app.project.name + ': ' + self.app.name + ' - ' + self.description[:50]
    
    class Meta:
        ordering = ['app', 'order']


class AppImage(models.Model):
    def get_image_path(instance, filename):
        return f'projects/{instance.project.name}/{instance.app.name}/{filename}'
    
    TYPES = (
        ('mobile-display', 'Mobile Display'),
        ('desktop-display', 'Desktop Display'),
        ('mobile-screenshot', 'Mobile Screenshot'),
        ('desktop-screenshot', 'Desktop Screenshot'),
        ('logo', 'Logo'),
        ('other', 'Other')
    )

    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='images')
    section = models.ForeignKey(AppSection, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, default='projects/default.png')
    type = models.CharField(max_length=20, choices=TYPES, default='other')

    def __str__(self):
        return self.app.project.name + ': ' + self.app.name + ' - ' + str(self.image)
    
    class Meta:
        ordering = ['app']


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    project = models.ForeignKey(Project, related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
    project_section = models.ForeignKey(ProjectSection, related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
    app = models.ForeignKey(App, related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
    app_section = models.ForeignKey(AppSection, related_name='snippets', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    highlighted = models.TextField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='monokai', max_length=100)

    class Meta:
        ordering = ['project', 'app', 'project_section', 'app_section']
        
    def __str__(self):
        if self.project:
            return f'{self.project} - {self.title}'
        
        elif self.project_section:
            return f'{self.project_section} - {self.title}'
        
        elif self.app:
            return f'{self.app} - {self.title}'
        
        elif self.app_section:
            return f'{self.app_section} - {self.title}'
        
        return self.title

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        formatter = HtmlFormatter(style=self.style, full=False, noclasses=True)
        self.highlighted = highlight(self.code, lexer, formatter)   
        super().save(*args, **kwargs)


