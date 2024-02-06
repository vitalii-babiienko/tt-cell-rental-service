import requests
from django.utils import timezone


def generate_random_cell_id(validation_error) -> int:
    try:
        response = requests.get(
            "https://csrng.net/csrng/csrng.php?min=1&max=50"
        )
        cell_id = response.json()[0].get("random")
    except Exception:
        raise validation_error(
            "Failed to generate a random cell_id!"
        )
    return cell_id


def validate_lease_end_time(
    start_time,
    end_time,
    validation_error,
) -> None:
    current_time = int(timezone.now().timestamp())

    if end_time <= start_time:
        raise validation_error(
            "end_time must be greater than start_time!"
        )

    if end_time <= current_time:
        raise validation_error(
            "end_time must be greater than current_time!"
        )
