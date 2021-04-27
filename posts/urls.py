from django.urls import path
from . import views


urlpatterns = (
    path('upload/', views.FileUploadView.as_view()),
    path('posts/', views.PostViewSet.as_view({
        'get': 'list',
        'post': 'create'
        })),
    path('posts/<int:pk>/', views.PostViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
        }), name='post-detail'),
    path('posts/<int:pk>/media/', views.PhotoViewSet.as_view({'get': 'list'})),
    path('posts/<int:pk>/media/<int:photo_pk>/', views.PhotoViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        }), name='photo-detail'),
    )
