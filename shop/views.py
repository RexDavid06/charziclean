from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from shop.models import Product, Category, CartItem
from django.views.generic.detail import DetailView
from .utils import get_or_create_cart
from .aliexpress_api import fetch_aliexpress_products

# Create your views here.
class HomeView(ListView):
    queryset = Category.objects.all()
    template_name = 'shop/home.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.all()[:8]
        return context
    
class ProductListView(TemplateView):
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch AliExpress products
        aliexpress_products = fetch_aliexpress_products(query="cleaning products")
        
        # Format for template
        formatted = []
        for item in aliexpress_products:
            formatted.append({
                'title': item.get('title', 'No name'),
                'brand': 'AliExpress',
                'price': item.get('price', '$0'),
                'image_url': item.get('image_url'),
                'product_url': item.get('product_url'),
            })

        context['products'] = formatted
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/productDetail.html'
    context_object_name = 'product'


class AboutUsView(TemplateView):
    template_name = 'shop/aboutUs.html'


class AddToCartView(View):
    def get(self, request, product_id):
        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, id=product_id)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            item.save()
        return redirect('cart_detail')

class RemoveFromCartView(View):
    def get(self, request, item_id):
        CartItem.objects.filter(id=item_id).delete()
        return redirect('cart_detail')

class CartDetailView(View):
    def get(self, request):
        cart = get_or_create_cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class AliExpressCleaningProductsView(View):
    template_name = 'shop/aliexpress_cleaning_products.html'

    def get(self, request, *args, **kwargs):
        products = fetch_aliexpress_products(query='cleaning products')
        print(products)  
        return render(request, self.template_name, {"poducts": products})