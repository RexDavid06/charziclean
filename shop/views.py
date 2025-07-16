from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from shop.models import Product, Category
from django.views.generic.detail import DetailView

# Create your views here.
class HomeView(ListView):
    queryset = Category.objects.all()
    template_name = 'shop/home.html'
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.all()[:8]
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'shop/shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/productDetail.html'
    context_object_name = 'product'


class AboutUsView(TemplateView):
    template_name = 'shop/aboutUs.html'
