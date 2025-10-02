from django.urls import path

from postal_card import views

urlpatterns = [
    path('', views.introduce, name='introduce_company')
]