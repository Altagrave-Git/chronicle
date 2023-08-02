from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Post)
admin.site.register(models.Title)
admin.site.register(models.Paragraph)
admin.site.register(models.Snippet)
admin.site.register(models.Image)
admin.site.register(models.Video)