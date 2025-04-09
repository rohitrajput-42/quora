from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "created", "updated", "author"]

admin.site.register(Post, PostAdmin)
admin.site.register(Question)
admin.site.register(Answer)