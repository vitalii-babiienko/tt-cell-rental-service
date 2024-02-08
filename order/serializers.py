from django.core.validators import EmailValidator
from rest_framework import serializers

from order.models import Order
from order.tasks import send_order_confirmation_email
from order.utils import generate_random_cell_id, validate_lease_end_time


class OrderCreateSerializer(serializers.ModelSerializer):
    user_data = serializers.DictField(write_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "slug",
            "start_timestamp",
            "end_timestamp",
            "user_email",
            "user_name",
            "cell_id",
            "reminded",
            "created_at",
            "user_data",
        )
        read_only_fields = (
            "id",
            "slug",
            "user_email",
            "user_name",
            "cell_id",
            "reminded",
            "created_at",
        )

    def validate_end_timestamp(self, value):
        start_timestamp = int(self.initial_data.get("start_timestamp"))

        validate_lease_end_time(
            start_timestamp,
            value,
            serializers.ValidationError,
        )

        return value

    def validate_user_data(self, value):
        email = value.get("email")
        name = value.get("name")

        if not email or not name:
            raise serializers.ValidationError(
                "Email and name are required!"
            )

        email_validator = EmailValidator()

        try:
            email_validator(email)
        except Exception as e:
            raise serializers.ValidationError({"email": e})

        return value

    def create(self, validated_data):
        validated_data["cell_id"] = (
            generate_random_cell_id(serializers.ValidationError)
        )

        user_data = validated_data.pop("user_data")
        validated_data["user_email"] = user_data.get("email")
        validated_data["user_name"] = user_data.get("name")

        order = Order.objects.create(**validated_data)

        send_order_confirmation_email.delay(order.id)

        return order
