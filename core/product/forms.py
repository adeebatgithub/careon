from django import forms

from core.models import Products


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ("default",)


class SelectProductForm(forms.Form):
    Product = forms.ModelChoiceField(queryset=Products.objects.all())
