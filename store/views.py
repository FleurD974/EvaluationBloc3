from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from store.models import Offer, Cart, Order

def index(request):
    offers = Offer.objects.all()
    return render(request, 'store/index.html', context={"offers": offers})

def offer_detail(request, slug):
    offer = get_object_or_404(Offer, offer_slug=slug)
    return render(request, 'store/detail.html', context={"offer": offer})

def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    return render(request, 'store/cart.html', context={"orders": cart.orders.all()})

# Pour ne pas que la vue est trop de logique, plus tard déplacer cette fonction dans le model de Customer et après ici on fait user.add_to_cart(slug)
def add_to_cart(request, slug):
    user = request.user
    offer = get_object_or_404(Offer, offer_slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user, ordered=False, offer=offer)
    
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()
        
    return redirect(reverse("offer", kwargs={"slug": slug}))

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
        
    return redirect('index')
