from django.urls import path

from .views import (
    post_action_view,
    PostList,
    # api_detail_blog_view,
    api_update_blog_view,
    api_delete_blog_view,
    api_create_blog_view
)


urlpatterns = [
    path('api/posts/action', post_action_view, name='api-action'),
    path('<slug>/', PostList.as_view(), name='detail'),
    # path('<slug>/', api_detail_blog_view, name='detail'),
    path('<slug>/update', api_update_blog_view, name='update'),
    path('<slug>/delete', api_delete_blog_view, name='delete'),
    path('create', api_create_blog_view, name='create'),
]
