from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("email/", views.SendEmailView.as_view(), name="email"),
    path("email/verify/", views.VerificationEmailView.as_view(), name="verify"),
]
