from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()


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
        ('found', 'found'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-date_added']


class Photo(models.Model):
    """Фото постов."""
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='photo', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'photo_pk': self.pk})

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"


class Tag(models.Model):
    """Тэги"""
    name = models.CharField(max_length=20, null=True, blank=True, unique=True)
    post = models.ManyToManyField(Post, related_name='tags', blank=True)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return str(self.name)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Comment(models.Model):
    """Комментарии к постам."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    text = models.TextField(null=False, blank=False)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL,
        blank=True, null=True, related_name='children'
    )

    def __str__(self):
        return f"{self.owner} - {self.text}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

