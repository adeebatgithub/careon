from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('add/', views.ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete'),
]
