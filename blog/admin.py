from django.contrib import admin
from . import models

admin.site.register(models.Post)
admin.site.register(models.Category)
admin.site.register(models.Subtitle)
admin.site.register(models.Paragraph)
admin.site.register(models.Image)
admin.site.register(models.Video)
admin.site.register(models.Snippet)
admin.site.register(models.Content)
admin.site.register(models.Link)