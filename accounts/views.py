from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import redirect, render

from accounts.forms import UserForm
from store.models import Order

User = get_user_model()

def signup(request):
    if request.method == "POST":
        #signup form treatment
        username =request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('index')
        
    return render(request, 'accounts/signup.html')

def login_user(request):
    if request.method == "POST":
        username =request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    if request.method == "POST":
        is_valid = authenticate(email=request.POST.get("email"), password=request.POST.get("password"))
        if is_valid:
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.save()
            messages.add_message(request, messages.SUCCESS, "Les informations ont été mises à jour")
        else:
            messages.add_message(request, messages.ERROR, "Le mot de passe n'est pas valide.")
        
        return redirect("accounts:profile")
    
    orders = Order.objects.filter(user=request.user)
    form = UserForm(initial=model_to_dict(request.user, exclude="password"))
    return render(request, 'accounts/profile.html', context={"form": form, "orders": orders})
