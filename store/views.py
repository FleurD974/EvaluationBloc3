from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from accounts.models import Customer
from store.forms import OrderForm
from store.models import Offer, Order

def index(request):
    offers = Offer.objects.all()
    return render(request, 'store/index.html', context={"offers": offers})

def about(request):
    return render(request, 'store/about.html')

def legal_notice(request):
    return render(request, 'store/legal.html')

def all_offers(request):
    offers = Offer.objects.all()
    return render(request, 'store/offers.html', context={"offers": offers})

def offer_detail(request, slug):
    offer = get_object_or_404(Offer, offer_slug=slug)
    return render(request, 'store/detail.html', context={"offer": offer})

@login_required
def cart(request):
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.count() == 0:
        return redirect('index')
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(queryset=orders)
    
    return render(request, 'store/cart.html', context={"forms": formset})

def update_quantities(request):
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
    formset = OrderFormSet(request.POST, queryset=Order.objects.filter(user=request.user))
    if formset.is_valid():
        formset.save()
        
    return redirect('store:cart')

def add_to_cart(request, slug):
    user: Customer = request.user
    user.add_to_cart(slug=slug)
        
    return redirect(reverse("store:offer", kwargs={"slug": slug}))

def delete_cart(request):
    if cart := request.user.cart:
        cart.delete()
        
    return redirect('index')

def create_checkout_session(request):
    cart = request.user.cart
    orders = cart.orders.all()
    items_in_cart = [{"price": order.offer.offer_price,
                        "quantity": order.quantity,
                        "name": order.offer.offer_name} for order in orders]
    total = 0
    for order in orders:
        total += order.offer.offer_price * order.quantity

    return render(request, 'store/checkoutSession.html', context={"items": items_in_cart, "total": total})

def checkout_success(request):
    # faire ici la mise à jour des order et tout après achat.
    request.user.cart.validate_cart()
    return render(request, 'store/success.html')

def conplete_order():
    pass
