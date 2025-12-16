from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from core.models import Products


class IndexView(RedirectView):
    permanent = True
    url = reverse_lazy('order:list')

    @staticmethod
    def create_products_if_not_exist():
        products = [
            {"name": "Product A", "reinforcement": Products.ATTACHED, "folding": Products.AMRITHA_FOLDING,
             "ties": Products.TIE_2},
            {"name": "Product B", "reinforcement": Products.ATTACHED, "folding": Products.NORMAL_FOLDING,
             "ties": Products.TIE_2},
            {"name": "Product C", "reinforcement": Products.ATTACHED, "folding": Products.AMRITHA_FOLDING,
             "ties": Products.TIE_4X6},
            {"name": "Product D", "reinforcement": Products.ATTACHED, "folding": Products.NORMAL_FOLDING,
             "ties": Products.TIE_4X6},
            {"name": "Product E", "reinforcement": Products.NOT_ATTACHED, "folding": Products.AMRITHA_FOLDING,
             "ties": Products.TIE_2},
            {"name": "Product F", "reinforcement": Products.NOT_ATTACHED, "folding": Products.NORMAL_FOLDING,
             "ties": Products.TIE_2},
            {"name": "Product G", "reinforcement": Products.NOT_ATTACHED, "folding": Products.AMRITHA_FOLDING,
             "ties": Products.TIE_4X6},
            {"name": "Product H", "reinforcement": Products.NOT_ATTACHED, "folding": Products.NORMAL_FOLDING,
             "ties": Products.TIE_4X6},
        ]
        for product in products:
            if not Products.objects.filter(name=product["name"]).exists():
                Products.objects.create(**product)

    def get(self, request, *args, **kwargs):
        self.create_products_if_not_exist()
        return super().get(request, *args, **kwargs)


class CalculateView(TemplateView):
    template_name = "result.html"
