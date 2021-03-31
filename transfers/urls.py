from django.contrib import admin
from django.urls import path, include

from transfers import views

urlpatterns = [
    path('', views.TransfersView.as_view(), name='transfers-list'),
    path('transfer/delete/<int:pk>/', views.TransferDeleteView.as_view(), name='transfer-delete'),
    path('transfer/update/<int:pk>/', views.TransferUpdateView.as_view(), name='transfer-update'),
    path('transfer/detail/<int:pk>/', views.TransferDetailView.as_view(), name='transfer-detail'),
]
