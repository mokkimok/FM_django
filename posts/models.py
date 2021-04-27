from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.reverse import reverse


class Post(models.Model):
    ANIMAL_KIND_CHOICES = [
        ('dogs', 'dogs'),
        ('cats', 'cats'),
    ]
    ANIMAL_SEX_CHOICES = [
        ('boy', 'boy'),
        ('girl', 'girl'),
    ]
    POST_TYPE_CHOICES = [
        ('lost', 'lost'),
        ('find', 'find'),
    ]

    date_added = models.DateTimeField(auto_now_add=True)
    date_event = models.DateTimeField(null=True, blank=True)
    post_type = models.CharField(max_length=20,
                                 choices=POST_TYPE_CHOICES, null=False,
                                 blank=False, default='lost')

    description = models.TextField(null=False, blank=True)
    animal_kind = models.CharField(max_length=20,
                                   choices=ANIMAL_KIND_CHOICES, null=False,
                                   blank=False)
    animal_sex = models.CharField(max_length=20,
                                  choices=ANIMAL_SEX_CHOICES, null=True,
                                  blank=True)
    castrated = models.BooleanField(null=True, blank=True)

    # Адрес
    lat = models.FloatField('Широта', blank=True, null=True)
    lng = models.FloatField('Долгота', blank=True, null=True)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return str(self.description[:40]) + ' ...'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Photo(models.Model):
    """Фото постов."""
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='photo', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'photo_pk': self.pk})


# class Tag(models.Model):
#     name = models.TextField(null=False, blank=True)
#     posts = models.ManyToManyField(Post, on_delete=models.CASCADE,
#                                    related_name='tags', null=True, blank=True)
