from django.urls import path

from .feeds import LatestPostsFeed
from . import views


urlpatterns = [
    path('blog/', views.PostListView.as_view(), name='post-list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('blog/category/<slug>/', views.PostCategoryView.as_view(), name='post-by-category'),
    path('blog/tag/<slug>/', views.PostTagView.as_view(), name='post-by-tag'),
    path('blog/<slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('blog/<slug>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('blog/<slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("category", views.CategoryView.as_view(), name="category-list"),
    path("tag", views.TagView.as_view(), name="tag-list"),
    path('getdata', views.getdata, name='getdata'),
    # path('serialized/', views.post_serialized_view, name='serialized-view'),
    # path('blog/<slug>/like/', views.PostLikeToggle.as_view(), name='like-toggle'),
    # path('api/<slug>/like/', views.PostLikeAPIToggle.as_view(), name='like-api-toggle'),
]
