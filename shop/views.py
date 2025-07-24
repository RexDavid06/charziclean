from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from shop.models import Product, Category, CartItem
from .utils import get_or_create_cart
from django.contrib import messages



class HomeView(ListView):
    queryset = Category.objects.all()
    template_name = 'shop/home.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.all()[:8]
        return context


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_queryset(self):
        category_id = self.request.GET.get("category")
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()


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
        return redirect('shop:cart_detail')


class RemoveFromCartView(View):
    def get(self, request, item_id):
        CartItem.objects.filter(id=item_id).delete()
        return redirect('shop:cart_detail')


class CartDetailView(View):
    def get(self, request):
        cart = get_or_create_cart(request)
        return render(request, 'shop/cart_detail.html', {'cart': cart})
    

class CheckoutView(TemplateView):
    template_name = 'shop/checkout.html'

    def get(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        if not cart.items.exists():
            messages.warning(request, "Your cart is empty!")
            return redirect('shop:cart_detail')
        return self.render_to_response({'cart': cart})

    def post(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        if not cart.items.exists():
            messages.warning(request, "Your cart is empty!")
            return redirect('shop:cart_detail')

        address = request.POST.get('address', '').strip()
        if not request.user.is_authenticated:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
        else:
            name = request.user.get_full_name() or request.user.username
            email = request.user.email

        # --- Save order to DB here and get order_id ---
        # Example:
        # order = Order.objects.create(
        #     user=request.user if request.user.is_authenticated else None,
        #     name=name, email=email, address=address,
        #     total=cart.total_price()
        # )
        # for item in cart.items.all():
        #     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        # cart.items.all().delete()
        # --- End Example ---

        # For now, let's use a placeholder order_id
        order_id = 1  # Replace with order.id after you implement Order model

        return redirect('shop:payment', order_id=order_id)


class PaymentView(TemplateView):
    template_name = 'shop/payment.html'

    def get(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        cart_items = cart.items.all()
        cart_total = cart.total_price()
        return self.render_to_response({
            'cart_items': cart_items,
            'cart_total': cart_total,
        })