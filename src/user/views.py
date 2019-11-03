from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from .forms import UserRegistrationForm, UserLoginForm


def display_logged_in_warning(request):
    if request.user.get_short_name():
        messages.warning(request, 'YOU ARE ALREADY LOGGED IN AS' + request.user.get_short_name().upper())
    else:
        messages.warning(request, 'YOU ARE ALREADY LOGGED IN')


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('index:index'))


class UserRegistrationFormView(View):
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'

    def get(self, request):
        if request.user.is_authenticated:
            display_logged_in_warning(request)

            return redirect(reverse_lazy('index:index'))

        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clean data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']

            user.set_password(password)
            user.save()

            messages.info(request, 'Your account has been created.')

            # log in registration
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_active:
                    return redirect(reverse_lazy('index:index'))

        return render(request, self.template_name, {'form': form})


class UserLoginFormView(View):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            display_logged_in_warning(request)

            return redirect('/')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            login(request, user)

            # displays the name of person logged in.
            if user.userprofile.first_name:
                messages.info(request, 'Welcome back, ' + str(user.userprofile.full_name()))

            else:
                messages.info(request, 'Welcome back, User')

            return redirect(reverse_lazy('index:index'))

        return render(request, self.template_name, {'form': form})
