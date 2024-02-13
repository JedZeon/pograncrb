from django.contrib import admin
from django.urls import path, include
from sign.views import ProfileView, ProfileEdit, upgrade_me

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls'), name='home'),

    path('accounts/', include('allauth.urls')),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileEdit.as_view(), name='profile_edit'),
    path('upgrade/', upgrade_me, name='upgrade')
]
