from django.urls import path

from .feeds import LatestPostsFeed
from .views import (
    SearchView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CategoryView,
    PostCategoryView,
    TagView,
    PostTagView,
)


urlpatterns = [
    path('blog/', PostListView.as_view(), name='post-list'),
    path('search/', SearchView.as_view(), name='search'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('blog/category/<slug>/', PostCategoryView.as_view(), name='post-by-category'),
    path('blog/tag/<slug>/', PostTagView.as_view(), name='post-by-tag'),
    path('blog/<slug>/', PostDetailView.as_view(), name='post-detail'),
    path('blog/<slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blog/<slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("category", CategoryView.as_view(), name="category-list"),
    path("tag", TagView.as_view(), name="tag-list"),
]
