from django.contrib import admin

from Task import models

# Register your models here.

admin.site.register(models.Task)
admin.site.register(models.User)
admin.site.register(models.Team)