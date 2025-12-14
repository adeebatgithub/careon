from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/', views.CalculateView.as_view(), name='result'),
    path('products/', include("core.product.urls")),
    path('order/', include("core.order.urls")),
]
