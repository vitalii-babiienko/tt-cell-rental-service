from django.test import TestCase

from order.forms import OrderForm


class TestOrderForm(TestCase):
    def test_valid_form(self):
        data = {
            "email": "john.dou@gmail.com",
            "name": "John",
            "start_date": "2024-02-01 19:05",
            "end_date": "2024-02-10 12:30",
        }
        form = OrderForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_date_format(self):
        data = {
            "email": "john.dou@gmail.com",
            "name": "John",
            "start_date": "202402101000",
            "end_date": "2024-02-10 12:30",
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = {
            "email": "john.dou.gmail.com",
            "name": "John",
            "start_date": "invalid",
            "end_date": "2024-02-10 12:30",
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())

    def test_start_time_gt_end_time(self):
        data = {
            "email": "john.dou@gmail.com",
            "name": "John",
            "start_date": "2024-02-10 19:05",
            "end_date": "2024-02-10 12:30",
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())
