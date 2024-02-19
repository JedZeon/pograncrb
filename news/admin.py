from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('date_time', 'title', 'author', 'rating')
    list_filter = ('date_time', 'author', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title',)


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
