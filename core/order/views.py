from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from core.base_views import BaseDeleteView
from core.models import Orders, OrderProducts, Products
from core.order.forms import OrderForm, OrderProductForm
from core.product.views import ProductCreateView


class OrderListView(ListView):
    model = Orders
    template_name = 'order/list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Orders
    template_name = 'order/detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'order/create.html'

    def get_success_url(self):
        return reverse_lazy('order:detail', kwargs={'pk': self.object.pk})


class OrderDeleteView(BaseDeleteView):
    model = Orders
    success_url = reverse_lazy("order:list")
    success_message = "order has been deleted"


class OrderProductCreateView(CreateView):
    model = OrderProducts
    form_class = OrderProductForm
    template_name = 'order/select.html'

    @staticmethod
    def get_products():
        products = Products.objects.all()
        products_data = {
            str(p.id): {
                'name': p.name,
                'reinforcement': p.get_reinforcement_display(),
                'folding': p.get_folding_display(),
                'ties': p.get_ties_display(),
            } for p in products
        }
        return products_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "pk": self.kwargs["pk"],
            "products": Products.objects.all(),
            "products_json": self.get_products(),
        })
        return context

    def get_success_url(self):
        return reverse_lazy('order:detail', kwargs={'pk': self.object.order.pk})

    def form_valid(self, form):
        order = Orders.objects.get(pk=self.kwargs['pk'])
        form.instance.order = order
        return super().form_valid(form)


class OrderProductUpdateView(UpdateView):
    model = OrderProducts
    form_class = OrderProductForm
    template_name = 'order/change.html'

    def get_success_url(self):
        return reverse_lazy('order:detail', kwargs={'pk': self.object.order.pk})


class OrderProductDeleteView(BaseDeleteView):
    model = OrderProducts
    success_message = "product has been deleted"

    def get_success_url(self):
        return reverse_lazy('order:detail', kwargs={'pk': self.object.order.pk})


class ProductAddView(ProductCreateView):
    template_name = "order/change.html"

    def get_success_url(self):
        return reverse_lazy('order:product-create', kwargs={'pk': self.kwargs['pk']})
