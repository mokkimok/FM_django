from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from .models import *


class UrlHyperlinkedIdentityField(HyperlinkedIdentityField):
    """Получение URL."""
    def get_url(self, obj, view_name, request, format):
        if obj.pk is None:
            return None
        if isinstance(obj, Post):
            kwargs = {'pk': obj.id}
        if isinstance(obj, Photo):
            kwargs = {
                'pk': obj.post.id,
                'photo_pk': obj.id
                      }
        return self.reverse(view_name, kwargs=kwargs, request=request,
                            format=format)


class PhotoListSerializer(serializers.ModelSerializer):
    """Вывод списка фото для поста."""
    url = UrlHyperlinkedIdentityField(view_name='photo-detail')

    class Meta:
        model = Photo
        fields = [
            'id',
            'image',
        ]


class PhotoSerializer(serializers.ModelSerializer):
    """Вывод одного фото для поста."""
    #url = UrlHyperlinkedIdentityField(view_name='photo-detail')

    class Meta:
        model = Photo
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Вывод поста."""
    url = UrlHyperlinkedIdentityField(view_name='post-detail')
    photo = PhotoListSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    """Вывод списка постов."""
    url = UrlHyperlinkedIdentityField(view_name='post-detail')
    photo = PhotoListSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'date_event',
            'date_added',
            'post_type',
            'animal_sex',
            'animal_kind',
            'castrated',
            'lat',
            'lng',
            'photo',
            'description',
        ]
