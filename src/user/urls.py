from django.urls import path

from .views import UserRegistrationFormView, UserLoginFormView, logout_view

app_name = 'user'

urlpatterns = [
    path('register/', UserRegistrationFormView.as_view(), name='register'),
    path('login/', UserLoginFormView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
