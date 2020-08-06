from django.urls import path
from .views import (
    my_profiles_view,
    invites_received_view,
    ProfileListView,
    invite_profiles_list_view,
)

urlpatterns = [
    path("myprofile/", my_profiles_view, name="my-profile"),
    path("my-invites/", invites_received_view, name="my-invites-view"),
    path("all-profile/", ProfileListView.as_view(), name="all-profile-view"),
    path("to-invite/", invite_profiles_list_view, name="invite-profile-view"),
]
