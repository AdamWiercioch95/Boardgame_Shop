from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import RegisterForm


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing_page')

        return render(request, 'accounts/register.html', {'form': form})
