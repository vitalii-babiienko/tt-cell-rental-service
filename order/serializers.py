import requests
from django.core.validators import EmailValidator
from django.utils import timezone
from rest_framework import serializers

from order.models import Order


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
        start_timestamp = int(self.initial_data.get("start_timestamp", None))
        current_timestamp = int(timezone.now().timestamp())

        if value <= start_timestamp or value <= current_timestamp:
            raise serializers.ValidationError(
                "end_timestamp must be greater than "
                "start_timestamp and current timestamp!"
            )
        return value

    def validate_user_data(self, value):
        email = value.get("email", None)
        name = value.get("name", None)

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
        try:
            response = requests.get(
                "https://csrng.net/csrng/csrng.php?min=1&max=50"
            )
            validated_data["cell_id"] = response.json()[0].get("random")
        except Exception:
            raise serializers.ValidationError(
                "Failed to generate a random cell_id!"
            )

        user_data = validated_data.pop("user_data")
        validated_data["user_email"] = user_data.get("email")
        validated_data["user_name"] = user_data.get("name")

        order = Order.objects.create(**validated_data)

        return order
