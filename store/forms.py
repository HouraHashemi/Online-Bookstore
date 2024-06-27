from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class BookSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)


class CartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
