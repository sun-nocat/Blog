from django.contrib import admin

# Register your models here.
from app import models

admin.site.register(models.User)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.ArticleImage)