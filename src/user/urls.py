from django.urls import path

from .views import UserRegistrationFormView, UserLoginFormView

app_name = 'user'

urlpatterns = [
    path('register/', UserRegistrationFormView.as_view(), name='register'),
    path('login/', UserLoginFormView.as_view(), name='login'),
]
