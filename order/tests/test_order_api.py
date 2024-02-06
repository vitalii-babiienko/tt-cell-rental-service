from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from order.models import Order

ORDER_CREATE_API_URL = reverse("order:order_create_api")


class TestCreateOrderAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_post_request(self):
        payload = {
            "start_timestamp": 1707000000,
            "end_timestamp": 1708000000,
            "user_data": {
                "email": "test@gmail.com",
                "name": "John",
            },
        }
        response = self.client.post(ORDER_CREATE_API_URL, payload, format="json")
        order = Order.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.user_email, payload["user_data"]["email"])
        self.assertEqual(order.user_name, payload["user_data"]["name"])

    def test_invalid_timestamps(self):
        payload = {
            "start_timestamp": 1708000001,
            "end_timestamp": 1708000000,
            "user_data": {
                "email": "test@example.com",
                "name": "John",
            },
        }
        response = self.client.post(ORDER_CREATE_API_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_invalid_email(self):
        payload = {
            "start_timestamp": 1707000000,
            "end_timestamp": 1708000000,
            "user_data": {
                "email": "notanemail",
                "name": "John",
            },
        }
        response = self.client.post(ORDER_CREATE_API_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
