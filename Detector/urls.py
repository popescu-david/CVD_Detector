from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient/<str:NSS>/', views.patient_detail, name='patient_detail'),
    path('about/', views.about, name='about'),
]