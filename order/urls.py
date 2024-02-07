from django.urls import path

from order.views import OrderCreateView, order_create_view, order_detail_view

urlpatterns = [
    path("api/v1/orders/", OrderCreateView.as_view(), name="order_create_api"),
    path("orders/", order_create_view, name="order_create"),
    path("orders/<slug>/", order_detail_view, name="order_detail"),
]

app_name = "order"
