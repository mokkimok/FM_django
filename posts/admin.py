from django.contrib import admin
from .models import Post, Photo, Tag, Comment

admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Comment)