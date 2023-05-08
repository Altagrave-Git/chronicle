from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    site = models.URLField()
    repo = models.URLField()

    def __str__(self):
        return self.name.replace(" ", "-")
    
    def get_absolute_url(self):
        # replace whitespace in self.name with hyphens
        return f'/projects/{self.name.replace(" ", "-")}/'
    
    class Meta:
        ordering = ['name']


class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    site = models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='apps')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class ProjectImage(models.Model):
    def get_image_path(instance, filename):
        return f'projects/{instance.project.name}/{filename}'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_image_path, default='projects/default.png')
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='images', null=True, blank=True)

    def __str__(self):
        return self.project.name + ' - ' + str(self.image)
    
    class Meta:
        ordering = ['project']