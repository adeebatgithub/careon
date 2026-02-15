from django.urls import path
from . import views

app_name = 'demand'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('<int:pk>/', views.OrderDeleteView.as_view(), name='delete'),

    path('product/add/', views.OrderProductCreateView.as_view(), name='product-create'),
    path('product/edit/<int:pk>/', views.OrderProductUpdateView.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', views.OrderProductDeleteView.as_view(), name='product-delete'),

    path('product/new/', views.ProductAddView.as_view(), name='product-new'),
]
