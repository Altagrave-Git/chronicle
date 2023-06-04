from django.contrib import admin
from . import models


admin.site.register(models.Project)
admin.site.register(models.ProjectSection)
admin.site.register(models.ProjectImage)
admin.site.register(models.Technology)
admin.site.register(models.Snippet)