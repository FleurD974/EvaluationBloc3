from django import forms

from accounts.models import Customer

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "password"]
        