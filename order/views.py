from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from rest_framework import generics

from order.forms import OrderForm
from order.models import Order
from order.serializers import OrderCreateSerializer
from order.utils import generate_random_cell_id


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


def order_create_view(request):
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            cell_id = generate_random_cell_id(ValidationError)

            order = Order.objects.create(
                start_timestamp=form.cleaned_data.get("start_date"),
                end_timestamp=form.cleaned_data.get("end_date"),
                user_email=form.cleaned_data.get("email"),
                user_name=form.cleaned_data.get("name"),
                cell_id=cell_id,
            )

            return redirect("order:order_detail", slug=order.slug)
    else:
        form = OrderForm()
    return render(request, "order/order_form.html", {"form": form})


def order_detail_view(request, slug):
    order = Order.objects.get(slug=slug)
    return render(request, "order/order_detail.html", {"order": order})
