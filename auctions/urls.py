from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('<int:pk>/', views.auction_detail, name='auction_detail'),
    path('<int:pk>/bid/', views.place_bid, name='place_bid'),
    path('<int:pk>/close/', views.close_auction, name='close_auction'),
    path('create/<int:product_pk>/', views.create_auction, name='create_auction'),
    path('<int:pk>/status/', views.auction_status, name='auction_status'),  # ← NEW
]
