from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2',)

        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            )

        }

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Passwords don\'t match')

        return password


class UserLoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)

        if not username_qs.exists():
            raise forms.ValidationError('Username does not exist. Create one using sign up link')

        return username

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(phone_number=username, password=password)

            if not user:
                raise forms.ValidationError("username or password is incorrect")

            if not user.is_active:
                raise forms.ValidationError("User is Banned.")

        return super(UserLoginForm, self).clean()
