from django.urls import path
from .views import my_profiles_view

urlpatterns = [
    path("myprofile/", my_profiles_view, name="my-profile")
]
