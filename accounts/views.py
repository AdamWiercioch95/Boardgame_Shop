from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm, LoginForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        context = {
            'form': form,
            'title': 'Register'
        }
        return render(request, 'accounts/form.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        context = {
            'form': form,
            'title': 'Register'
        }

        if form.is_valid():
            form.save()
            return redirect('login')

        return render(request, 'accounts/form.html', context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form': form,
            'title': 'Login'
        }
        return render(request, 'accounts/form.html', context)

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('landing_page')
            else:
                form.add_error(None, 'Username or password is incorrect')

        context = {
            'form': form,
            'title': 'Login'
        }
        return render(request, 'accounts/form.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')
