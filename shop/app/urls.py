from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:order_pk>/', views.checkout, name='checkout'),
]