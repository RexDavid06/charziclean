from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ProductListView.as_view(), name='shop'),
    path('details/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('aboutUs/', views.AboutUsView.as_view(), name='aboutUs'),
    path('cart_detail/', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'), 
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<int:order_id>/', views.PaymentView.as_view(), name='payment'),
]