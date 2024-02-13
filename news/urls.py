from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryList

urlpatterns = [
    path('', PostList.as_view()),
    path('news/', PostList.as_view(), name="post_list"),
    path('news/<int:pk>', PostDetail.as_view(), name="post_detail"),
    path('news/search/', PostSearch.as_view(), name="post_search"),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe', CategoryList.subscribe_user, name='subscribe'),
    path('category/<int:pk>/unsubscribe', CategoryList.unsubscribe_user, name='unsubscribe'),
]
