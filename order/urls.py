from django.urls import path

from order.views import OrderCreateView

urlpatterns = [
    path("api/v1/orders/", OrderCreateView.as_view(), name="order_create_api")
]

app_name = "order"
