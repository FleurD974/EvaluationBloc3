from django.shortcuts import get_object_or_404, render

from store.models import Offer

def index(request):
    offers = Offer.objects.all()
    return render(request, 'store/index.html', context={"offers": offers})

def offer_detail(request, slug):
    offer = get_object_or_404(Offer, offer_slug=slug)
    return render(request, 'store/detail.html', context={"offer": offer})