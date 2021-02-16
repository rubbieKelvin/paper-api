from . import models
from django.contrib import admin

# Register your models here.
admin.site.register(models.Checkbook)
admin.site.register(models.CheckbookMembership)
admin.site.register(models.TextItem)
admin.site.register(models.ImageItem)
admin.site.register(models.AudioItem)
admin.site.register(models.ChecklistItem)
admin.site.register(models.CheckItem)