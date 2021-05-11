from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from .models import Post, Photo, Tag, Comment


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


class FilterCommentsListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents. """
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Вывод комментариев."""
    children = RecursiveSerializer(many=True)
    # owner = serializers.CurrentUserDefault

    class Meta:
        model = Comment
        fields = '__all__'


class PhotoListSerializer(serializers.ModelSerializer):
    """Вывод списка фото для поста."""
    # url = UrlHyperlinkedIdentityField(view_name='photo-detail')

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


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'name',
        ]

    def to_representation(self, obj):
        return obj.name


class PostSerializer(serializers.ModelSerializer):
    """Вывод поста."""
    url = UrlHyperlinkedIdentityField(view_name='post-detail')
    photo = PhotoListSerializer(many=True)
    tags = TagListSerializer(many=True)
    comments = CommentSerializer(many=True)
    owner = serializers.CurrentUserDefault

    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    """Вывод списка постов."""
    url = UrlHyperlinkedIdentityField(view_name='post-detail')
    photo = PhotoListSerializer(many=True)
    tags = TagListSerializer(many=True)
    owner = serializers.CurrentUserDefault

    class Meta:
        model = Post
        fields = '__all__'
