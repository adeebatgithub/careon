from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

class IndexView(RedirectView):
    permanent = True
    url = reverse_lazy('order:list')


class CalculateView(TemplateView):
    template_name = "result.html"
