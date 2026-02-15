from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/<int:pk>/', views.ResultView.as_view(), name='result'),
    path('result/demand/<int:pk>/', views.DemandResult.as_view(), name='demand-result'),
    path('products/', include("core.product.urls")),
    path('order/', include("core.order.urls")),
    path('demand/', include("core.demand.urls")),
]
