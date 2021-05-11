from .serializers import *
from rest_framework import viewsets, views, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    """Представления постов."""
    queryset = Post.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Post.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        try:
            tags = request.data.pop('tags')
        except BaseException:
            tags = []
        new_post = Post.objects.create(**request.data, owner=request.user)
        for tag in tags:
            try:
                instance = Tag.objects.get(name=tag)
            except BaseException:
                instance = Tag.objects.create(name=tag)
            instance.post.add(new_post)
        serializer = PostSerializer(new_post, context={'request': request})
        url = str(serializer.data.get('url'))
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers={'Location': url})

    def destroy(self, request, pk=None, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=200)


class FileUploadView(views.APIView):
    """Загрузка фото с привязкой к id поста."""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def put(self, request, format=None):
        post_id = request.data.get('id')
        images = request.FILES.getlist('file')
        for image in images:
            photo = Photo.objects.create(image=image,
                                         post=Post.objects.get(pk=post_id))
            serializer = PhotoSerializer(photo, context={'request': request})
        return Response(status=status.HTTP_201_CREATED)


class PhotoViewSet(viewsets.ModelViewSet):
    """Представления фото."""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_fields = ('pk', 'photo_pk')

    def list(self, request, pk=None, photo_pk=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        queryset = Photo.objects.filter(post=post)
        serializer = PhotoListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, photo_pk=None, *args, **kwargs):
        photo = Photo.objects.get(pk=photo_pk)
        post = Post.objects.get(pk=pk)
        if photo.post.id != post.id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset = Photo.objects.get(pk=photo_pk)
        serializer = PhotoSerializer(queryset, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None, photo_pk=None, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        Photo.objects.get(pk=photo_pk).delete()
        return Response(status=200)


class CommentsViewSet(viewsets.ModelViewSet):
    """Представления комментариев."""
    queryset = Comment.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = CommentSerializer
    lookup_fields = ('pk', 'comment_pk')

    def list(self, request, pk=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        queryset = self.filter_queryset(Comment.objects.filter(post=post, parent=None))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, comment_pk=None,  *args, **kwargs):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=comment_pk)
        if comment.post.id != pk:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def create(self, request, pk=None, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        post = Post.objects.get(pk=pk)
        parent = None
        if 'parent' in request.data:
            parent_pk = request.data.pop('parent')
            parent = Comment.objects.get(pk=parent_pk)
        new_comment = Comment.objects.create(**request.data, post=post,
                                             owner=request.user,
                                             parent=parent)
        serializer = CommentSerializer(new_comment, context={'request': request})
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, comment_pk=None, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()
        return Response(status=200)