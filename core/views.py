import math
from collections import defaultdict

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from core.models import Products, Orders, OrderProducts
from .calc import number_of_workers, next_even, total_number_of_workers


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


class ResultView(TemplateView):
    template_name = "result.html"

    def get_order(self):
        return get_object_or_404(Orders, pk=self.kwargs['pk'])

    def get_products(self):
        return OrderProducts.objects.filter(order=self.get_order())

    def total_number_of_workers_per_activity(self):
        workers_per_activity = defaultdict(lambda: {"default": 0.0, "required": 0.0})

        for product in self.get_products():
            workers = number_of_workers(
                demand=product.demand,
                nos_tie=product.product.ties,
                folding_type=product.product.folding,
                attached=product.product.reinforcement
            )

            for activity, counts in workers.items():
                workers_per_activity[activity]["required"] += counts["required"]
                workers_per_activity[activity]["default"] = counts["default"]

        rounded_total = {}
        for activity, counts in workers_per_activity.items():
            name = activity.replace("_", " ").title()
            rounded_total[name] = {
                "required": math.ceil(counts["required"]),
                "default": counts["default"],
            }

        for activity in ("welcrow_attachment", "reinforcement_attachment", "tie_attachment"):
            name = activity.replace("_", " ").title()
            if name in rounded_total:
                rounded_total[name]["required"] = next_even(rounded_total[name]["required"])

        return rounded_total

    def total_number_of_workers(self):
        number_of_workers_per_activity = self.total_number_of_workers_per_activity()
        total = 0
        for activity, counts in number_of_workers_per_activity.items():
            total += counts["required"]

        return total

    def overtime(self):
        additional_workers = self.total_number_of_workers() - 105
        if additional_workers > 0:
            return math.ceil((additional_workers * 480) / 105)
        return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "total_number_of_workers": self.total_number_of_workers(),
            "order": self.get_order(),
            "workers": self.total_number_of_workers_per_activity(),
            "overtime": self.overtime(),
        })
        return context


class DemandResult(TemplateView):
    template_name = "demand_result.html"

    def get_order(self):
        return get_object_or_404(Orders, pk=self.kwargs['pk'])

    def get_product(self):
        return self.get_order().products().first()

    def get_mul_factor(self, activity, folding):
        if activity == "body_cuff_cutting":
            return 3
        elif activity in ("welcrow_attachment", "reinforcement_attachment", "tie_attachment"):
            return 2
        elif activity == "folding" and folding == 1:
            return 2
        return 1

    def get_demand(self):
        product = self.get_product()
        for n in range(1, 99999):
            workers, workers_list = total_number_of_workers(
                demand=n,
                nos_tie=product.product.ties,
                folding_type=product.product.folding,
                attached=product.product.reinforcement
            )
            if workers >= product.demand + 1:
                return n, workers_list
        return 0, None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workers, workers_list = self.get_demand()
        context.update({
            "demand": round(workers),
            "workers": self.get_product().demand,
            "workers_list": workers_list,
            "total_number_of_workers": self.get_product().demand
        })
        return context
