from django import forms

from core.models import Orders, OrderProducts


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = "__all__"


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProducts
        exclude = ("order",)
