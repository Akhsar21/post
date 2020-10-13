from django.urls import path
from .views import (
    my_profiles_view,
    invites_received_view,
    ProfileDetailView,
    ProfileListView,
    invite_profiles_list_view,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation,
)

urlpatterns = [
    path("", ProfileListView.as_view(), name="all-profile-view"),
    path("myprofile/", my_profiles_view, name="my-profile"),
    path("my-invites/", invites_received_view, name="my-invites-view"),
    path("to-invite/", invite_profiles_list_view, name="invite-profile-view"),
    path("send-invite/", send_invitation, name="send-invite"),
    path("remove-friend/", remove_from_friends, name="remove-friend"),
    path("<slug>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("my-invites/accept/", accept_invitation, name="accept-invite"),
    path("my-invites/reject/", reject_invitation, name="reject-invite"),
]
