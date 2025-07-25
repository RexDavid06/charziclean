from shop.utils import get_or_create_cart

def cart_item_count(request):
    cart = get_or_create_cart(request)
    return {
        'cart_item_count': cart.items.count() if cart else 0
    }