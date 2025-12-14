from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from core.models import Products
from .forms import ProductForm
from ..base_views import BaseDeleteView


class ProductListView(ListView):
    queryset = Products.objects.filter(default=True)
    template_name = 'products/list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Products
    template_name = 'products/detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Products
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('product:list')


class ProductUpdateView(UpdateView):
    model = Products
    form_class = ProductForm
    template_name = 'products/update.html'
    success_url = reverse_lazy('product:list')


class ProductDeleteView(BaseDeleteView):
    model = Products
    success_url = reverse_lazy('product:list')
    success_message = "product successfully deleted"
