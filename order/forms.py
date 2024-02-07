from django import forms

from order.utils import validate_lease_end_time


class OrderForm(forms.Form):
    email = forms.EmailField(label="Email")
    name = forms.CharField(label="Name")
    start_date = forms.DateTimeField(
        label="Start of lease",
        widget=forms.DateTimeInput(
            format="%d.%m.%y %H:%M",
            attrs={"type": "datetime-local"}
        ),
        input_formats=["%d.%m.%y %H:%M"]
    )
    end_date = forms.DateTimeField(
        label="End of lease",
        widget=forms.DateTimeInput(
            format="%d.%m.%y %H:%M",
            attrs={"type": "datetime-local"}
        ),
        input_formats=["%d.%m.%y %H:%M"]
    )

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_date")
        end_time = cleaned_data.get("end_date")

        if start_time and end_time:
            cleaned_data["start_date"] = int(start_time.timestamp())
            cleaned_data["end_date"] = int(end_time.timestamp())

            validate_lease_end_time(
                cleaned_data["start_date"],
                cleaned_data["end_date"],
                forms.ValidationError,
            )

        return cleaned_data
