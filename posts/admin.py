from django.contrib import admin
from .models import Post, Photo, Tag

admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Tag)