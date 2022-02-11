from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from . import forms
from . import models


class MainView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:user', kwargs={'username': request.user.username}))
        return HttpResponseRedirect(reverse('users:login'))


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(reverse('users:main'))
        
        messages.error(self.request, 'Username or password incorrect')
        return HttpResponseRedirect(reverse('users:main'))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('users:main'))


class RegistrationView(FormView):
    template_name = "users/registration.html"
    form_class = forms.RegistrationForm

    def form_valid(self, form):
        if form.cleaned_data['password'] == form.cleaned_data['repeat_password']:
            user = form.save(commit=False)
            user.is_active = False
            user.password = make_password(user.password)
            user.save()
            registration = models.UserRegistration.objects.update_or_create(user=user)
            return HttpResponseRedirect(reverse('users:main'))

        return self.form_invalid(form)


class OnlineView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_activity, _ = models.UserOnline.objects.update_or_create(user=request.user)
            user_activity.save()
            return HttpResponse(status=200)
        return HttpResponse(status=500)


class UserView(LoginRequiredMixin, View):
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(models.User, username=username)
        return render(request, 'users/user.html', {'user': user})
