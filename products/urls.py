from django.urls import path

from .views import (
    chart_select_view,
    PurchaseCreateView,
    sales_dist_view
)

urlpatterns = [
    path("", chart_select_view, name="chart"),
    path("add", PurchaseCreateView.as_view(), name="add-purchase-view"),
    path("sales", sales_dist_view, name="sales-view")
]
