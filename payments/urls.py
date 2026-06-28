from django.urls import path
from . import views

urlpatterns = [
    path('<int:auction_pk>/', views.payment_page, name='payment_page'),
    path('<int:auction_pk>/cancel/', views.payment_cancel, name='payment_cancel'),
]