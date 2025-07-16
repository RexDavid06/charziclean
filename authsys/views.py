from django.shortcuts import render
from authsys.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'authsys/register.html'
    success_url = reverse_lazy('authsys:signin')


class SigninView(LoginView):
    form_class = LoginForm
    template_name = 'authsys/signin.html'


class SignoutView(LogoutView):
    next_page = 'shop:home'


