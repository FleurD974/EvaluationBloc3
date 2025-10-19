from django.urls import path
from store.views import offer_detail, add_to_cart, cart, delete_cart, create_checkout_session, checkout_success, update_quantities

app_name = "store"

urlpatterns = [
    path('cart/', cart, name="cart"),
    path('cart/update_quantities', update_quantities, name="update-quantities"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('cart/create-checkout-session', create_checkout_session, name="create-checkout-session"),
    path('cart/success', checkout_success, name="checkout-success"),
    path('offers/<str:slug>', offer_detail, name="offer"),
    path('offers/<str:slug>/add-to-cart', add_to_cart, name="add-to-cart"),
]
