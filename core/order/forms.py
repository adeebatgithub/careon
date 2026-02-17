from django import forms

from core.models import Orders, OrderProducts


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ("is_reverse", )


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProducts
        exclude = ("order",)
