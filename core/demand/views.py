from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView

from core.base_views import BaseDeleteView
from core.models import Orders, OrderProducts, Products
from core.order import views
from core.order.forms import OrderProductForm
from core.product.views import ProductCreateView


class OrderListView(views.OrderListView):
    queryset = Orders.objects.filter(is_reverse=True)
    template_name = 'demand/list.html'


class OrderDeleteView(views.OrderDeleteView):
    success_url = reverse_lazy("demand:list")


class OrderProductCreateView(CreateView):
    model = OrderProducts
    form_class = OrderProductForm
    template_name = 'demand/select.html'

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
            "products": Products.objects.all(),
            "products_json": self.get_products(),
        })
        return context

    def get_success_url(self):
        return reverse_lazy('demand:list')

    def form_valid(self, form):
        order = Orders.objects.create(
            name=str(timezone.localtime()),
            is_reverse=True,
        )
        form.instance.order = order
        return super().form_valid(form)


class OrderProductUpdateView(UpdateView):
    model = OrderProducts
    form_class = OrderProductForm
    template_name = 'demand/change.html'

    def get_success_url(self):
        return reverse_lazy('order:list')


class OrderProductDeleteView(BaseDeleteView):
    model = OrderProducts
    success_message = "product has been deleted"

    def get_success_url(self):
        return reverse_lazy('order:list')


class ProductAddView(ProductCreateView):
    template_name = "demand/change.html"

    def get_success_url(self):
        return reverse_lazy('demand:product-create')
