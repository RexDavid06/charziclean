from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ProductListView.as_view(), name='shop'),
    path('details/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('aboutUs/', views.AboutUsView.as_view(), name='aboutUs')
]
