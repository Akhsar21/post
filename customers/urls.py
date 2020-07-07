from django.urls import path
from .views import customer_corr_view

urlpatterns = [
    path("", customer_corr_view, name="customer-view")
]
