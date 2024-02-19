from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    categories = models.ManyToManyField('Category', through='PostCategory', verbose_name='Категории (несколько)')
    date_time = models.DateField(verbose_name='Создан')
    likes = models.IntegerField(default=0, verbose_name='+')
    dislikes = models.IntegerField(default=0, verbose_name='-')
    rating = models.FloatField(default=0, verbose_name='рейтинг')

    # img = models.ImageField(upload_to='')
    # pdf = models.FileField(upload_to='')

    class Meta:
        ordering = ('-date_time',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'{self.date_time.strftime("%d.%m.%Y")}: {self.title}'

    def preview(self):
        return f'{self.content[0:124]}...'

    def like(self):
        self.likes += 1
        self.rating += 1
        self.save()

    def dislike(self):
        self.dislikes += 1
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('post-by-category', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)  # вызываем сохранение как и должно было быть
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.user

    def update_rating(self):
        articles_rate = int((Post.objects.filter(author_id=self.pk).aggregate(Sum('rate'))['rate__sum'] * 3) or 0)
        comment_rate = int(Comment.objects.filter(user_id=self.user).aggregate(Sum('rate'))['rate__sum'] or 0)
        comments_posts_rate = int(
            Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rate'))['rate__sum'] or 0)

        self.rating = articles_rate + comment_rate + comments_posts_rate
        self.save()

        return self.rating

    def update_sum_post(self):
        return Post.objects.filter(author=self).count()


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, related_name='children', null=True, blank=True,
                            verbose_name='Родительская категория')
    slug = models.SlugField(max_length=150, unique=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])

    def __str__(self):
        return self.title


class SubscriberCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    rating = models.FloatField(default=0)

    def __str__(self):
        return f'{self.date_added.strftime("%d.%m.%Y")}: {self.text}'
