from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm,UserPasswordResetForm,UserSetPasswordForm

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Users/password_reset/password_reset.html', form_class=UserPasswordResetForm),name='password_reset'),
    path('password-reset/done/',views.pw_reset_done,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Users/password_reset/password_reset_confirm.html', form_class=UserSetPasswordForm),name='password_reset_confirm'),
    path('password-reset/complete/',views.pw_reset_complete,name='password_reset_complete'),
]