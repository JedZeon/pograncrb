from allauth.account.forms import LoginForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Author, Post, Comment
from django.views.generic.edit import CreateView, UpdateView
from .models import ChangeForm, BasicSignupForm
from django.contrib.auth.decorators import login_required


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        # При добавлении пользователя как автора - создать объект таблицы автора
        if not Author.objects.filter(id=user.id).exists():
            author = Author.objects.create(user=user)
    return redirect('/')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        if not context['is_not_authors']:
            author = Author.objects.get(user=self.request.user)
            # пересчет рейтинга
            context['rate'] = author.update_rating()
            # Подсчет количества публикаций
            context['sum_post'] = author.update_sum_post()
            # Лучшая новость
            best_news = Post.objects.order_by('-rate').first()
            context['best_news'] = best_news
            context['best_news_preview'] = best_news.preview()
            context['best_news_rate'] = best_news.preview()
        return context


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ChangeForm
    model = User
    template_name = 'account/profile_edit.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
